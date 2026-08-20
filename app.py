from flask import Flask, render_template, jsonify
import json
from datetime import datetime

app = Flask(__name__)

def load_data():
    with open("opportunities.json", "r", encoding="utf-8") as file:
        return json.load(file)

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

if __name__ == "__main__":
    app.run(debug=True)