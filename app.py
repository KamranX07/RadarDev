from flask import Flask, render_template, jsonify
import json
import os
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BRIGHTDATA_API_KEY=os.getenv("BRIGHTDATA_API_KEY")
BRIGHTDATA_COLLECTOR_ID=os.getenv("BRIGHTDATA_COLLECTOR_ID")

app = Flask(__name__)

def load_data():
    with open("opportunities.json", "r", encoding="utf-8") as file:
        return json.load(file)

def fetch_collection(collection_id):
    url = "https://api.brightdata.com/dca/dataset"

    headers = {
        "Authorization": f"Bearer {BRIGHTDATA_API_KEY}"
    }

    for attempt in range(60):
        response = requests.get(
            url,
            params={"id": collection_id},
            headers=headers,
            timeout=30
        )

        response.raise_for_status()
        raw_text = response.text.strip()
        print(
            f"Dataset check {attempt + 1}/60 - "
            f"status={response.status_code}"    
        )

        if not raw_text:
            print("Empty response, waiting...")
            time.sleep(5)
            continue

        try:
            data = response.json()
            if isinstance(data, list):
                print(f"Collection ready: {len(data)} records")
                return data

            if isinstance(data, dict) and "name" in data:
                print("Collection returned a single record.")
                return [data]
            
            print(f"Collection status: {data}")

        except requests.exceptions.JSONDecodeError:
            records = []

            for line in raw_text.splitlines():
                line = line.strip()

                if not line:
                    continue

                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

            if records:
                print(f"Collection ready: {len(records)} records")
                return records
            print("Could not parse dataset yet.")

        time.sleep(5)

    raise RuntimeError(
        "Bright Data collection did not finish within 5 minutes."
    )

@app.route("/")
def home():
    opportunities = load_data()

    return render_template(
        "index.html",
        opportunities=opportunities
    )

@app.route("/api/opportunities")
def api_opportunities():
    opportunities = load_data()
    return jsonify(opportunities)

@app.route("/health")
def health():
    opportunities = load_data()

    required_fields = [
        "name",
        "mode",
        "status",
        "participation_count",
        "hackathon_url"
    ]

    optional_fields = [
        "themes",
        "start_date"
    ]

    total_records = len(opportunities)

    missing_required = []

    for item in opportunities:
        for field in required_fields:
            value = item.get(field)

            # 0 is valid for participation_count
            if value is None:
                missing_required.append(field)
            elif isinstance(value, str) and not value.strip():
                missing_required.append(field)

    missing_optional = 0
    total_optional = total_records * len(optional_fields)

    for item in opportunities:
        for field in optional_fields:
            value = item.get(field)

            if value is None:
                missing_optional += 1
            elif isinstance(value, str) and not value.strip():
                missing_optional += 1

    # Calculate quality
    quality = 100

    if total_optional > 0:
        quality -= (missing_optional / total_optional) * 10

    if missing_required:
        quality -= 50

    quality = round(max(0, quality), 1)

    if quality >= 90:
        status = "healthy"
    elif quality >= 70:
        status = "degraded"
    else:
        status = "critical"

    return jsonify({
        "status": status,
        "records": total_records,
        "data_quality": quality,
        "missing_required_fields": list(set(missing_required)),
        "optional_missing": missing_optional,
        "checked_at": datetime.now().isoformat(timespec="seconds")
    })

@app.route("/refresh", methods=["POST"])
def refresh():
    if not BRIGHTDATA_API_KEY or not BRIGHTDATA_COLLECTOR_ID:
        return jsonify({
            "success": False,
            "error": "Bright Data configuration is missing"
        }), 500

    trigger_url = "https://api.brightdata.com/dca/trigger"

    params = {
        "collector": BRIGHTDATA_COLLECTOR_ID,
        "queue_next": 1
    }

    payload = [
        {
            "url": "https://devfolio.co/hackathons"
        }
    ]

    headers = {
        "Authorization": f"Bearer {BRIGHTDATA_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # 1. Trigger Bright Data
        response = requests.post(
            trigger_url,
            params=params,
            json=payload,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()
        print("STATUS: ", response.status_code)
        print("CONTENT TYPE: ", response.headers.get("content-type"))
        print("RAW RESPONSE: ")
        print(response.text)
        response_data = response.json()

        collection_id = response_data.get("collection_id")

        if not collection_id:
            return jsonify({
                "success": False,
                "error": "Bright Data did not return a collection_id",
                "bright_data_response": response_data
            }), 500

        print(f"Collection started: {collection_id}")

        # 2. Wait for the collection to finish
        data = fetch_collection(collection_id)

        # 3. Save fresh results locally
        with open(
            "opportunities.json",
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2
            )

        print(f"Saved {len(data)} records to opportunities.json")

        # 4. Return success
        return jsonify({
            "success": True,
            "collector_id": BRIGHTDATA_COLLECTOR_ID,
            "collection_id": collection_id,
            "records": len(data),
            "message": "Hackathons refreshed successfully"
        })

    except requests.RequestException as error:
        return jsonify({
            "success": False,
            "error": f"Bright Data request failed: {str(error)}"
        }), 500

    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)