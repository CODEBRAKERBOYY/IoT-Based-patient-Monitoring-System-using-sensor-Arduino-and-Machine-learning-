import requests

url = "http://127.0.0.1:5000/data"

data = {
    "BPM": 72,
    "SPO2": 98,
    "Body_Temp": 36.5,
    "Ambient_Temp": 28,
    "Humidity": 60
}

response = requests.post(url, json=data)
print(response.json())