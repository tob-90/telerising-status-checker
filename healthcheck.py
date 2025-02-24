#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
import re
import logging
import json

app = Flask(__name__)

# Telerising-Endpoint und Passwort bitte anpassen
base_url = "http://127.0.0.1:5000"
password = "secret1234"

login_url = f"{base_url}/api/login_check"
timeout = 10

logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET'])
def healthcheck():
    try:
        # Login und Cookies
        response = requests.post(login_url, data={"pw": password}, timeout=timeout)
        response.raise_for_status()

        session_cookies = response.cookies.get_dict()
        session_id = session_cookies.get("sessionID", None)
        session = session_cookies.get("session", None)

        if not session_id or not session:
            logging.error("Erforderliche Cookies fehlen.")
            return jsonify({"error": "Erforderliche Cookies fehlen"}), 500

        # HTML-Quellcode abholen
        cookies = {"session": session, "sessionID": session_id}
        status_response = requests.get(base_url, cookies=cookies, timeout=timeout)
        status_response.raise_for_status()

        # HTML-Quellcode parsen
        soup = BeautifulSoup(status_response.text, 'html.parser')
 
        data = []

        # JavaScript-Code extrahieren
        for script in soup.find_all('script', type='text/javascript'):
            for line in script.text.splitlines():
                line = line.strip()
                if line.startswith('var test ='):
                    json_string = line.replace('var test =', '').replace(';', '').strip()
                    json_obj = json.loads(json_string)
                    for key in json_obj.keys():
                        data.append({
                            "Account": json_obj[key]['info']['type'],
                            "Provider": key,
                            "Status": json_obj[key].get('status', None),
                            "Success": json_obj[key].get('success', None)
                        })

        if all(item['Success'] for item in data):
            status_value = "healthy"
        else:
            status_value = "unhealthy"

        # Providers formatieren
        providers = {}

        for item in data:
            providers[item["Provider"]] = {
                "Account": item["Account"],
                "Status": item["Status"],
                "Success": item["Success"]
            }

        return jsonify({"status": status_value, "Providers": providers}), 200 if status_value == "healthy" else 500    

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP-Fehler: {e}")
        return jsonify({"error": "HTTP-Fehler", "details": str(e)}), 500
    except Exception as e:
        logging.error(f"Allgemeiner Fehler: {e}")
        return jsonify({"error": "Allgemeiner Fehler", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
