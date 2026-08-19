from flask import Flask, render_template
import json

app = Flask(__name__)

with open("opportunities.json", "r", encoding="utf-8") as file:
    opportunities = json.load(file)

@app.route("/")
def home():
    return render_template(
        "index.html",
        opportunities=opportunities
    )

if __name__ == "__main__":
    app.run(debug=True)