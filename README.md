# Telerising Status Checker

This Python script provides a Flask-based API endpoint that checks the health status of a Telerising web application.
The primary focus is on monitoring the availability and health of the providers integrated within the Telerising service.

![Healthcheck](https://github.com/user-attachments/assets/11c22cc6-50ea-4656-a35a-2adc63a64ee5)

## Features
- Logs into the Telerising service using an API endpoint
- Identifies status indicators using regex patterns
- Monitors the status of integrated providers
- Returns a JSON response indicating the health status

## Installation
### Requirements
This script requires Python 3 and the following dependencies:

```bash
pip install requests beautifulsoup4 flask
```

## Configuration
Modify the following parameters in the script as needed:
- `base_url`: The base URL of the Telerising service (default: `http://127.0.0.1:5000`)
- `password`: The authentication password for login

### Setup
1. Copy the file `healthcheck.py` to a folder of your choice.
2. Make the script executable:
   ```bash
   chmod +x healthcheck.py
   ```

## Running the Application
Start the Flask application & running in background using:
```sh
python3 healthcheck.py & disown
```
The API will be accessible at `http://0.0.0.0:5555/`.

## Monitoring Integration
The health check endpoint can be integrated into monitoring software such as **Uptime Kuma**. By configuring Uptime Kuma to periodically check the endpoint, automatic alerts can be triggered whenever the service status is reported as **unhealthy**. This allows for real-time monitoring and automated notifications in case of failures. The monitoring primarily ensures that the providers integrated within the Telerising service are operational and responsive.

![uptime_kuma](https://github.com/user-attachments/assets/70b31add-ca7c-46d9-a36c-ddebc9734897)

## Disclaimer
> [!CAUTION]
> This script is provided "as is," without any warranties or guarantees. The author is not responsible for any data loss or unintended consequences resulting from the use of this script. Users are responsible for configuring and testing the script to ensure it meets their needs. Use at your own risk.
