import requests

# Replace with your Mist API credentials
# UseCase 3:-List of users having signal strength more than -70DBM
# add field for SSID & filter based on strength between 30 to 50

MIST_API_TOKEN = 'xh9oBdbYQllXCmCh5Ad63h3Y3enrewPWrDD37XpYA5f1ealYTPJQEb2FMkmo0DBi9vFIiLJpNlHd6fM95Zog8e0NldKTnOol'
ORG_ID = '15e7597e-9b06-4381-8443-16aba95c5e0d'
SITE_ID = 'a631d811-8b9b-48ef-823b-b5594e4af356'

def get_live_users():
    headers = {
        'Authorization': f'Token {MIST_API_TOKEN}'
    }
    url = f'https://api.eu.mist.com/api/v1/sites/{SITE_ID}/stats/clients'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        clients = response.json()
        strong_signal_clients = [client for client in clients if client.get('rssi', -100) < -70]
        
        for client in strong_signal_clients:
            print(f"Client: {client.get('mac')}, Signal Strength: {client.get('rssi')}")
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    get_live_users()
