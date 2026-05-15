import serial
import re
import csv

ser = serial.Serial("COM6", 9600, timeout=1)

file = open("iot_data.csv", "a", newline="")
writer = csv.writer(file)

print("Logging clean IoT data...\n")

while True:
    try:
        line = ser.readline().decode(errors="ignore").strip()

        if not line:
            continue

        # IGNORE boot / garbage lines
        if "WiFi" in line or "Connecting" in line or "FAILED" in line:
            continue

        # DEBUG print
        print("RAW:", line)

        # Extract values from your existing Arduino text
        bpm = re.search(r"Heart rate:([0-9.]+)", line)
        spo2 = re.search(r"SpO2:([0-9.]+)", line)
        body = re.search(r"Body Temperture: ([0-9.]+)", line)
        ambient = re.search(r"Ambient Temperature: ([0-9.]+)", line)
        hum = re.search(r"Humidity: ([0-9.]+)", line)

        if bpm and spo2 and body and ambient and hum:
            row = [
                bpm.group(1),
                spo2.group(1),
                body.group(1),
                ambient.group(1),
                hum.group(1)
            ]

            writer.writerow(row)
            file.flush()

            print("✅ SAVED:", row)

    except Exception as e:
        print("Error:", e)