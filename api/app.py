from flask import Flask, jsonify
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

@app.route("/api/opportunities", methods=["GET"])
def opportunities():
    try:
        with open("scraped.json", "r") as file:
            data = json.load(file)
        file.close()
    except:
        return {}
    return data

@app.route("/api/opportunities/<opportunity_id>", methods=["GET"])
def get_opportunity(opportunity_id):
    opportunity = next((o for o in opportunities() if o["id"] == opportunity_id), None)
    if opportunity:
        return jsonify(opportunity)
    else:
        return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(port=5000)