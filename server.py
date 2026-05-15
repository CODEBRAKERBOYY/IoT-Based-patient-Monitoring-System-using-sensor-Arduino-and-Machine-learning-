from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)

DATA_FILE = "iot_data.csv"

@app.route("/data", methods=["POST"])
def receive_data():
    data = request.json

    new_row = {
        "r_id": None,
        "reg_no": "LIVE_DEVICE",
        "field_value3": str({
            "884": str(data.get("BPM")),
            "885": str(data.get("SPO2")),
            "886": str(data.get("Body_Temp")),
            "887": str(data.get("Ambient_Temp")),
            "888": str(data.get("Humidity"))
        }).replace("'", '"'),
        "p_id": None,
        "iot_date": datetime.now()
    }

    try:
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    except:
        df = pd.DataFrame([new_row])

    df.to_csv(DATA_FILE, index=False)

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)