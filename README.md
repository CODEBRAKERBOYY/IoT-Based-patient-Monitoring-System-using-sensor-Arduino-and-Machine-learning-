# 🏥 IoT Based Health Monitoring System using sensor Arduino and machine learning 

A smart and real-time IoT solution designed to continuously measure and monitor vital human health parameters.  
This system collects Heart Rate, Blood Pressure, and Body Temperature data using biomedical sensors and transmits it to a cloud server for remote monitoring and anomaly detection.

---

## 📌 Project Overview
The **IoT Based Health Monitoring System** enables 24×7 health observation without requiring the patient to be physically present in hospitals.  
Live sensor readings are uploaded to a cloud database and visualized on a dashboard, allowing doctors/caregivers to monitor patient status remotely.  
Whenever a health-related abnormality occurs, the system can trigger alerts for early intervention.

---

## 🎯 Key Features
- Real-time monitoring of **Heart Rate, Blood Pressure & Body Temperature**
- Wireless transmission of sensor data via **ESP8266 / ESP32 Wi-Fi module**
- **Cloud database integration** for storing health records
- **Interactive dashboard** to display health values graphically
- **Threshold-based anomaly alerts** for abnormal readings
- **Low-cost, scalable & portable design**
- Can be used for **home healthcare, elderly care & emergency assistance**

---

## 🏗 System Architecture
The system integrates:
- Biomedical sensors → microcontroller → Wi-Fi module → cloud server → web dashboard

(Architecture and DFD are based on the project report — Page 17 & 18 :contentReference[oaicite:0]{index=0})

---

## 🛠 Tech Stack

| Category | Tools / Components |
|----------|--------------------|
| Microcontroller | Arduino Uno / NodeMCU / ESP32 |
| Sensors | BP Sensor, Heart Rate Sensor (MAX30102), Temperature Sensor (LM35 / DS18B20) |
| Connectivity | ESP8266 Wi-Fi Module |
| Backend | Firebase / Thingspeak / MySQL |
| Frontend | HTML, CSS, JavaScript |
| IDE | Arduino IDE |

---

## 📡 Data Pipeline
1. Sensors collect physiological signals  
2. Microcontroller converts them into digital data  
3. Data sent to cloud server via Wi-Fi  
4. Dashboard fetches and visualizes data in charts  
5. Alert triggered if a value exceeds threshold  

---

## 📍 Installation & Setup

### 🔧 Hardware
1. Connect BP, Temperature & Heart Rate sensors to Arduino/ESP pins
2. Configure Wi-Fi credentials in Arduino code
3. Upload firmware via Arduino IDE

### 💻 Software
1. Clone this repository
2. Configure Firebase / Thingspeak / MySQL credentials
3. Run the web dashboard
4. Power the device → live values appear on screen

---

## 📊 Dashboard Preview
(Add screenshots here after deployment)

---

## 🚨 Anomaly Detection
Alerts are generated when:
- Heart Rate > 120 BPM or < 60 BPM  
- Body Temperature > 38°C or < 36°C  
- BP values beyond normal threshold  

(alert logic based on system description in the PDF — Page 13 :contentReference[oaicite:1]{index=1})



---

## 📌 Future Enhancements
- Integration with wearable IoT devices
- AI-based prediction of health risks
- Mobile app support
- ECG & SpO2 sensor compatibility

---

## 🏁 Conclusion
This project presents a low-cost yet efficient IoT-based system for real-time health monitoring, scalable for both home and clinical applications. It helps reduce hospital burden while improving accessibility to healthcare.

