#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
import re
import logging

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

        # Finde IDs, die mit '-status' enden
        status_elements = soup.find_all(id=re.compile(r'.*-status$'))

        # Filtere nach IDs, die nicht '-card-status' enthalten
        status_elements = [el for el in status_elements if '-card-status' not in el.get('id', '')]

        # Finde IDs, die mit '-account-text' enden
        account_text_elements = soup.find_all(id=re.compile(r'.*-account-text$'))

        # Extrahieren der Statuswerte
        status_values = {}
        account_text_values = {}

        for status_element in status_elements:
            status_id = status_element.get('id')
            status_values[status_id] = status_element.text.strip()

        for account_text_element in account_text_elements:
            account_text_id = account_text_element.get('id')
            account_text_values[account_text_id] = account_text_element.text.strip()

        # Prüfung, ob Status OK ist und der account-text 'Unknown' enthält
        for status_id, status_value in status_values.items():
            if status_value == "OK":
                # Wenn der Status "OK" ist und der account-text "Unknown" liefert, dann unhealthy
                account_text_value = account_text_values.get(status_id.replace("-status", "-account-text"), None)
                if account_text_value == "Unknown":
                    return jsonify({"status": "unhealthy", "details": {"status": status_values, "account-text": account_text_values}}), 500

        # Ansonsten Status healthy
        return jsonify({"status": "healthy", "details": {"status": status_values, "account-text": account_text_values}}), 200

    except requests.exceptions.RequestException as e:
        logging.error(f"HTTP-Fehler: {e}")
        return jsonify({"error": "HTTP-Fehler", "details": str(e)}), 500
    except Exception as e:
        logging.error(f"Allgemeiner Fehler: {e}")
        return jsonify({"error": "Allgemeiner Fehler", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
