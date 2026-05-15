<div align="center">

# 🏥 IoT-Based Patient Health Monitoring System
### Real-Time Vital Sign Monitoring + Machine Learning Anomaly Detection

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit)](https://streamlit.io)
[![Flask](https://img.shields.io/badge/Flask-API-black?logo=flask)](https://flask.palletsprojects.com)
[![ML Model](https://img.shields.io/badge/ML-Isolation%20Forest-green?logo=scikit-learn)](https://scikit-learn.org)
[![Arduino](https://img.shields.io/badge/Hardware-Arduino%20%2F%20ESP32-teal?logo=arduino)](https://arduino.cc)
[![License](https://img.shields.io/badge/License-Academic-orange)](#)

*Final Year Project — Registration: 25PSITCS011*

</div>

---

## 📷 Hardware Setup

<p align="center">
  <img src="hardware_photo.jpg" width="500" alt="IoT Hardware Board"/>
</p>

> **Assembled perf board** featuring a MAX30100 pulse oximeter, DHT11 temperature & humidity sensor, SIM800L GSM module, 16×2 I2C LCD display, and a 6V–12V buzzer — powered by a DC jack supply.

---

## 📌 Project Overview

This project builds a **complete end-to-end IoT health monitoring pipeline**:

- 🔴 **Hardware sensors** collect patient vitals continuously — heart rate, SpO₂, body temperature, ambient temperature, and humidity
- 📡 **NodeMCU ESP32** processes sensor data and transmits it via USB Serial or SIM800L GSM module (SMS every 30 seconds)
- 🖥️ **Python backend** (Flask + reader.py) receives, stores, and feeds live data into a CSV
- 🤖 **Isolation Forest ML model** automatically flags abnormal reading patterns without needing labelled data
- 📊 **Streamlit dashboard** streams live readings with Normal / Abnormal status and instant alert banners
- 🔔 **Buzzer + LCD** give immediate local feedback on the device itself

> **Why it matters:** Manual monitoring is slow and misses gradual deterioration. This system enables 24×7 continuous observation with early-warning anomaly detection at very low hardware cost — ideal for home care, elderly monitoring, and hospital assistance.

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────┐
│                   HARDWARE LAYER                     │
│                                                      │
│    MAX30100 Sensor          DHT11 Sensor             │
│    ├─ Heart Rate (BPM)      ├─ Body Temperature      │
│    └─ SpO₂ (%)              ├─ Ambient Temperature   │
│                             └─ Humidity (%)          │
│                                                      │
│              NodeMCU ESP32 / Arduino                 │
│         (reads all sensors, formats output)          │
│              │                     │                 │
│         USB Serial            SIM800L GSM            │
│              │              (SMS every 30s)          │
└──────────────┼─────────────────────────────────────--┘
               │
               ▼
┌──────────────────────────────────────────────────────┐
│                  SOFTWARE LAYER                      │
│                                                      │
│   reader.py  ←── reads Arduino USB serial output    │
│   server.py  ←── receives HTTP POST from GSM/WiFi   │
│         │                                            │
│         └──────────► iot_data.csv (118 records)     │
│                             │                        │
│                    ML Pipeline                       │
│         ┌───────────────────┴──────────────────┐    │
│    Clean Data (median fill)   StandardScaler    │    │
│         └───────────────────┬──────────────────┘    │
│                    Isolation Forest                  │
│                  anomaly_model.pkl                   │
│                             │                        │
│                   Normal  /  Abnormal                │
└─────────────────────────────┼────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────┐
│           STREAMLIT DASHBOARD  (app.py)              │
│   Live data table  │  BPM vs SpO₂ chart              │
│   Anomaly count    │  🚨 Alert banners                │
└──────────────────────────────────────────────────────┘
```

---

## 📦 Hardware Components

| Component | Role | Detail |
|---|---|---|
| **NodeMCU ESP32** | Main microcontroller | Reads all sensors, manages WiFi + Serial output |
| **MAX30100** | Heart Rate + SpO₂ | Optical pulse oximeter sensor |
| **DHT11** | Temperature + Humidity | ±2°C, ±5% RH accuracy |
| **SIM800L GSM Module** | Wireless SMS alerts | Sends readings every 30 seconds |
| **16×2 LCD (I2C)** | On-device live display | Shows current readings locally |
| **6V–12V Buzzer** | Local alarm | Triggers instantly on abnormal readings |
| **Perf Board + DC Supply** | Assembly + power | Compact portable build |

---

## 📊 Sensor Parameters Monitored

| Field ID | Parameter | Unit | Healthy Range |
|---|---|---|---|
| `884` | Heart Rate (BPM) | beats/min | 60 – 100 |
| `885` | SpO₂ (Blood Oxygen) | % | 95 – 100 |
| `886` | Body Temperature | °C | 36.1 – 37.2 |
| `887` | Ambient Temperature | °C | Environmental |
| `888` | Humidity | % | Environmental |

---

## 🤖 Machine Learning — Anomaly Detection

### Model Summary

| Property | Value |
|---|---|
| **Algorithm** | Isolation Forest (Unsupervised) |
| **Library** | scikit-learn |
| **Contamination rate** | 10% |
| **Preprocessing** | StandardScaler |
| **Train / Test Split** | 80% / 20% → 93 train, 24 test |
| **Dataset** | 118 real sensor readings (May 2026) |
| **Test Result** | ✅ 22 Normal, 🚨 2 Abnormal detected |
| **Saved files** | `anomaly_model.pkl`, `scaler.pkl` |

### Why Isolation Forest?

Isolation Forest is **unsupervised** — it learns what "normal" looks like from your own sensor data and flags anything that deviates. No need to manually label "abnormal" cases. This makes it perfect for health monitoring where abnormal readings are rare and unpredictable.

### Full ML Training Pipeline (`iot_project.ipynb`)

```
Raw CSV → 118 readings with JSON-encoded field_value3
         │
         ▼
  Parse JSON → extract BPM, SPO2, Body_Temp, Ambient_Temp, Humidity
         │
         ▼
  Data Cleaning
   ├─ Zero values → NaN  (BPM: 56 zeros, SPO2: 64 zeros found)
   ├─ Fill NaN with column median
   └─ IQR clipping on BPM to remove outliers
         │
         ▼
  EDA — Histograms, Correlation Heatmap, Boxplots
         │
         ▼
  StandardScaler → normalize all 5 features
         │
         ▼
  Isolation Forest (contamination=0.1, random_state=42)
   └─ Trained on 93 samples
         │
         ▼
  Predict on 24 test samples
   └─ Output: "Normal" or "Abnormal" per reading
         │
         ▼
  Save → anomaly_model.pkl + scaler.pkl
```

---

## 🗂️ Project Structure

```
IoT-Based-patient-Monitoring-System/
│
├── 📓 iot_project.ipynb          ← ML training notebook (Google Colab)
├── 🤖 anomaly_model.pkl          ← Trained Isolation Forest model
├── ⚖️  scaler.pkl                ← Fitted StandardScaler
│
├── 📊 iot_data.csv               ← 118 real sensor readings (May 2026)
│
├── 🌐 server.py                  ← Flask REST API (receives POST from ESP32/GSM)
├── 🔌 reader.py                  ← Reads Arduino serial data → CSV
├── 🧪 send_test_data.py          ← Simulate sensor data without hardware
│
├── 📺 app.py                     ← Streamlit live dashboard
├── 📑 iot_health_monitoring_presentation.pptx
└── 📄 README.md
```

---

## 🚀 Setup & Running

### 1. Install Dependencies

```bash
pip install streamlit flask pandas numpy scikit-learn matplotlib seaborn joblib pyserial requests
```

### 2. With Real Hardware

**Start Flask server** (receives data from ESP32/GSM module):
```bash
python server.py
# Runs on http://0.0.0.0:5000
# Your ESP32 should POST JSON to: http://<your-pc-ip>:5000/data
```

**OR read directly from Arduino via USB serial:**
```bash
python reader.py
# Default: COM6 at 9600 baud
# Mac/Linux: change to /dev/ttyUSB0 or /dev/cu.usbserial-*
```

### 3. Without Hardware (Demo / Test Mode)

```bash
# Terminal 1
python server.py

# Terminal 2
python send_test_data.py   # sends sample reading to the server
```

### 4. Launch the Dashboard

```bash
streamlit run app.py
```
Open **http://localhost:8501** in your browser.

---

## 📺 Streamlit Dashboard Features

| Feature | Description |
|---|---|
| 📡 **Live Data Stream** | Scrolling real-time table of all sensor readings |
| ✅ **Normal Counter** | Running total of normal readings |
| 🚨 **Abnormal Counter** | Running total of anomalies flagged by ML model |
| 🔔 **Alert Banner** | Red warning displayed immediately when anomaly found |
| 📈 **BPM vs SpO₂ Scatter** | Visual separation of Normal vs Abnormal points |
| ⏱️ **Refresh Speed Slider** | Adjustable 1–5 second update interval |
| 📁 **CSV Upload** | Upload any new CSV to run the model on fresh data |

---

## 📡 Flask API Reference

**Endpoint:** `POST /data`

**Request (JSON from ESP32/GSM):**
```json
{
  "BPM": 72,
  "SPO2": 98,
  "Body_Temp": 36.5,
  "Ambient_Temp": 28.0,
  "Humidity": 60
}
```

**Response:**
```json
{ "status": "success" }
```

Each POST is automatically appended to `iot_data.csv` with a timestamp.

---

## 📊 Dataset Statistics

| Metric | Value |
|---|---|
| Total Records | 118 readings |
| Collection Period | May 4–5, 2026 |
| Device ID | 25PSITCS011 |
| BPM Range | 0 – 83.35 bpm |
| SpO₂ Range | 0 – 99% |
| Body Temperature | 19.31 – 33.81 °C |
| Humidity | 0 – 65% |
| Invalid BPM zeros cleaned | 56 values (filled with median) |
| Invalid SpO₂ zeros cleaned | 64 values (filled with median) |

---

## 📸 Images to Add to This README

> Take these screenshots and add them to the repo with the names below:

| Filename | What to Capture |
|---|---|
| `hardware_photo.jpg` | Physical board photo ✅ already added |
| `dashboard_normal.png` | Streamlit running — showing all-normal readings |
| `dashboard_alert.png` | Streamlit with red 🚨 anomaly alert triggered |
| `anomaly_scatter.png` | BPM vs SpO₂ scatter plot from dashboard or notebook |
| `correlation_heatmap.png` | Feature correlation heatmap from Colab notebook |
| `boxplot.png` | Boxplot after data cleaning (from notebook) |

To add an image to README after uploading to repo:
```markdown
![Dashboard](dashboard_normal.png)
```

---

## 🔮 Future Enhancements

- [ ] Mobile app (Flutter / React Native) for remote patient alerts
- [ ] ECG sensor integration for deeper cardiac monitoring
- [ ] Automatic SMS alerts via Twilio when anomaly is detected
- [ ] Multi-patient dashboard with login system
- [ ] LSTM deep learning for time-series anomaly prediction
- [ ] Cloud deployment on AWS IoT Core or Google Cloud IoT

---

## 👥 Team

| | Detail |
|---|---|
| **Registration** | 25PSITCS011 |
| **Hardware** | NodeMCU ESP32, MAX30100, DHT11, SIM800L GSM |
| **ML** | Isolation Forest — scikit-learn |
| **Dashboard** | Streamlit |
| **Backend** | Flask |
| **Data** | 118 real sensor readings collected May 2026 |

---

## 📄 License

This project was developed for academic and final year project purposes.

---

<div align="center">

**⭐ If this project helped you, please give it a star on GitHub!**

*Built with ❤️ using IoT + Python + Machine Learning*

</div>
