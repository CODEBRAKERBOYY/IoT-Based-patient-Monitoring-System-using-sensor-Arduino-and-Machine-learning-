# 🩺 IoT Health Monitoring System with ML Anomaly Detection

A real-time IoT-based health monitoring system that collects vital signs and environmental data from hardware sensors, transmits it to a server, and uses a Machine Learning model (Isolation Forest) to detect anomalies — with live visualization via a Streamlit dashboard.

---

## 📷 Hardware Setup

![IoT Hardware Board](hardware_photo.jpg)

> The physical device includes a DHT11 sensor, MAX30100 pulse oximeter, SIM800L GSM module, 6V–12V buzzer, and a 16×2 LCD display — all mounted on a perf board.

---

## 🧩 System Architecture

```
[Sensors: MAX30100 + DHT11]
        ↓
[Arduino/Microcontroller]
        ↓  (Serial / GSM)
[reader.py / server.py]  ←→  iot_data.csv
        ↓
[ML Model: Isolation Forest]
        ↓
[Streamlit Dashboard: app.py]
```

---

## 📦 Hardware Components

| Component | Purpose |
|---|---|
| MAX30100 Pulse Oximeter | Measures Heart Rate (BPM) and SpO₂ |
| DHT11 Sensor | Measures Body Temperature, Ambient Temperature, and Humidity |
| SIM800L GSM Module | Wireless data transmission |
| 16×2 LCD (I2C) | Local display of readings |
| 6V–12V Buzzer | Alert on abnormal readings |
| Perf Board + Power Supply | Hardware assembly |

---

## 📊 Sensor Data Collected

| Field ID | Parameter | Unit |
|---|---|---|
| 884 | Heart Rate (BPM) | beats/min |
| 885 | SpO₂ (Blood Oxygen) | % |
| 886 | Body Temperature | °C |
| 887 | Ambient Temperature | °C |
| 888 | Humidity | % |

---

## 🤖 Machine Learning Model

- **Algorithm:** Isolation Forest (Unsupervised Anomaly Detection)
- **Library:** scikit-learn
- **Contamination Rate:** 10%
- **Preprocessing:** StandardScaler (fit on training data only)
- **Train/Test Split:** 80/20
- **Saved Models:** `anomaly_model.pkl`, `scaler.pkl`

### How it works:
1. Raw sensor data is parsed and cleaned (zeros replaced with median values)
2. IQR-based outlier clipping applied to BPM
3. Features scaled with StandardScaler
4. Isolation Forest flags readings as **Normal** or **Abnormal**

---

## 🗂️ Project Structure

```
IOT PROJECT/
│
├── iot_project.ipynb        # ML training notebook (Google Colab)
├── anomaly_model.pkl        # Trained Isolation Forest model
├── scaler.pkl               # Fitted StandardScaler
│
├── iot_data.csv             # Collected sensor data (118 records)
│
├── reader.py                # Reads serial data from Arduino → CSV
├── server.py                # Flask API server (receives POST data)
├── send_test_data.py        # Test script to simulate device data
│
└── app.py                   # Streamlit real-time dashboard
```

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install streamlit flask pandas numpy scikit-learn matplotlib seaborn joblib pyserial requests
```

### 2. Start the Flask Server (to receive hardware data)

```bash
python server.py
```

> Runs on `http://0.0.0.0:5000`. The Arduino/GSM module POSTs data to `/data`.

### 3. Read Serial Data from Arduino (if connected via USB)

```bash
python reader.py
```

> Connects to `COM6` at 9600 baud. Update the port as needed for your system.

### 4. Send Test Data (without hardware)

```bash
python send_test_data.py
```

### 5. Launch the Dashboard

```bash
streamlit run app.py
```

---

## 📈 Dashboard Features

- 📡 **Live Data Stream** — real-time scrolling table of all sensor readings
- ✅ / 🚨 **Anomaly Counter** — Normal vs Abnormal reading counts
- 🔔 **Instant Alert** — red banner when abnormal health readings are detected
- 📉 **BPM vs SpO₂ Scatter Plot** — visual separation of normal and anomalous points
- ⏱️ **Adjustable Refresh Rate** — 1–5 second slider

---

## 🔬 ML Notebook Workflow (`iot_project.ipynb`)

1. Load `iot_data.csv` and parse JSON field values
2. Extract features: BPM, SpO₂, Body Temp, Ambient Temp, Humidity
3. Data cleaning: replace zeros with `NaN`, fill with median
4. Visualize: histograms, correlation heatmap, boxplots
5. IQR-based BPM outlier clipping
6. Train/test split → StandardScaler → Isolation Forest
7. Predict anomalies and visualize scatter plot
8. Save model and scaler as `.pkl` files

---

## 🖼️ Screenshots to Include in README

> Add these images to make your README complete:

| Image | What to Capture |
|---|---|
| `hardware_photo.jpg` | Physical board (already shown above) |
| `dashboard_screenshot.png` | Streamlit running with live data table and chart |
| `anomaly_scatter.png` | BPM vs SpO₂ scatter plot (Normal vs Abnormal) |
| `correlation_heatmap.png` | Feature correlation heatmap from notebook |
| `architecture_diagram.png` | System flow diagram (optional) |

---

## 👥 Team

- **Registration No.:** 25PSITCS011
- **Dataset:** 118 real sensor readings collected from hardware (May 2026)

---

## 📄 License

This project was developed for academic/educational purposes.
