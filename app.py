import streamlit as st
import pandas as pd
import numpy as np
import json
import joblib
import matplotlib.pyplot as plt
import time

# Page config
st.set_page_config(page_title="IoT Health Dashboard", layout="wide")

st.title("🩺 IoT Health Monitoring Dashboard")

# Upload option
uploaded_file = st.file_uploader("📁 Upload IoT CSV File", type=["csv"])

# Load model
model = joblib.load("anomaly_model.pkl")
scaler = joblib.load("scaler.pkl")

# Load data
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    try:
        df = pd.read_csv("iot_data.csv")
    except:
        st.warning("Waiting for IoT data...")
        st.stop()

# Parse JSON column
df["parsed"] = df["field_value3"].apply(lambda x: json.loads(x))

# Extract features
df["BPM"] = df["parsed"].apply(lambda x: float(x.get("884", 0)))
df["SPO2"] = df["parsed"].apply(lambda x: float(x.get("885", 0)))
df["Body_Temp"] = df["parsed"].apply(lambda x: float(x.get("886", 0)))
df["Ambient_Temp"] = df["parsed"].apply(lambda x: float(x.get("887", 0)))
df["Humidity"] = df["parsed"].apply(lambda x: float(x.get("888", 0)))

# Clean data
df_clean = df[["BPM", "SPO2", "Body_Temp", "Ambient_Temp", "Humidity"]]
df_clean = df_clean.replace(0, np.nan)
df_clean = df_clean.fillna(df_clean.median())

# Scale and predict
X_scaled = scaler.transform(df_clean)
preds = model.predict(X_scaled)

df_clean["Status"] = ["Normal" if x == 1 else "Abnormal" for x in preds]

# Refresh control
refresh_rate = st.slider("⏱️ Refresh Speed (seconds)", 1, 5, 2)

# Placeholder for live data
placeholder = st.empty()

# Real-time simulation loop
for i in range(len(df_clean)):
    current_data = df_clean.iloc[:i+1]

    with placeholder.container():
        st.subheader("📡 Live IoT Data Stream")

        # Metrics
        normal_count = (current_data["Status"] == "Normal").sum()
        abnormal_count = (current_data["Status"] == "Abnormal").sum()

        col1, col2 = st.columns(2)
        col1.metric("✅ Normal Readings", normal_count)
        col2.metric("🚨 Abnormal Readings", abnormal_count)

        # Alert
        if abnormal_count > 0:
            st.error("🚨 ALERT: Abnormal health readings detected!")
        else:
            st.success("✅ All readings are normal")

        # Data table
        st.dataframe(current_data)

        # Visualization
        st.subheader("📈 Anomaly Visualization")

        fig, ax = plt.subplots()

        normal = current_data[current_data["Status"] == "Normal"]
        abnormal = current_data[current_data["Status"] == "Abnormal"]

        ax.scatter(normal["BPM"], normal["SPO2"], label="Normal")
        ax.scatter(abnormal["BPM"], abnormal["SPO2"], label="Abnormal")

        ax.set_xlabel("BPM")
        ax.set_ylabel("SPO2")
        ax.legend()

        st.pyplot(fig)

    time.sleep(refresh_rate)