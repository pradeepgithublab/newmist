import requests
import matplotlib.pyplot as plt

# Replace with your Mist API credentials
# UseCase 3:-List of users having signal strength more than -70DBM

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
        strong_signal_clients = [client for client in clients if client.get('rssi', -100) > -70]
        return strong_signal_clients
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

def plot_clients(clients):
    mac_addresses = [client['mac'] for client in clients]
    rssi_values = [client['rssi'] for client in clients]

    plt.figure(figsize=(10, 5))
    plt.bar(mac_addresses, rssi_values, color='blue')
    plt.xlabel('Client MAC Addresses')
    plt.ylabel('Signal Strength (dBm)')
    plt.title('Users with Signal Strength Greater Than -70 dBm')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    clients = get_live_users()
    if clients:
        plot_clients(clients)
