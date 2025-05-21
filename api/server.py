from flask import Flask, jsonify
import pandas as pd
from pathlib import Path
import os

app = Flask(__name__)

ENRICHED_DIR = Path("data/enriched_products")

def get_latest_csv():
    files = list(ENRICHED_DIR.glob("enriched_*.csv"))
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)

@app.route("/get-products", methods=["GET"])
def get_products():
    latest_csv = get_latest_csv()
    if not latest_csv:
        return jsonify({"error": "Zenginleştirilmiş CSV dosyası bulunamadı."}), 404
    
    df = pd.read_csv(latest_csv)
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(port=port, debug=True)
