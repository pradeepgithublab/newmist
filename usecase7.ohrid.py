import requests
import json

# Define your Mist API credentials and organization ID
api_token = 'xh9oBdbYQllXCmCh5Ad63h3Y3enrewPWrDD37XpYA5f1ealYTPJQEb2FMkmo0DBi9vFIiLJpNlHd6fM95Zog8e0NldKTnOol'
org_id = '15e7597e-9b06-4381-8443-16aba95c5e0d'

# Headers for the API requests
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Token {api_token}'
}

# Define the list of VIP user MAC addresses or user IDs
vip_users = ['fe3f36fd2560', 'bc5c17351258']  # replace with actual MAC addresses or user IDs

def get_wifi_metrics_for_vip_users():
    vip_metrics = {}

    for user in vip_users:
        # Get the client's connection details
        response = requests.get(
            f'https://api.eu.mist.com/api/v1/orgs/{org_id}/stats/devices?mac={user}',
            headers=headers
        )

        if response.status_code == 200:
            client_data = response.json()
            if client_data and len(client_data) > 0:
                client_info = client_data[0]  # Assuming the first entry is the relevant one
                vip_metrics[user] = {
                    'client_name': client_info.get('device_name', 'N/A'),
                    'mac_address': client_info.get('mac', 'N/A'),
                    'connected_ssid': client_info.get('ssid', 'N/A'),
                    'signal_strength': client_info.get('rssi', 'N/A'),
                    'data_usage': client_info.get('bytes_used', 'N/A'),
                    'last_seen': client_info.get('last_seen', 'N/A'),
                    # Add more fields as needed
                }
            else:
                vip_metrics[user] = 'No data available for this user'
        else:
            vip_metrics[user] = f"Failed to retrieve data. Status code: {response.status_code}"

    return vip_metrics

def main():
    vip_metrics = get_wifi_metrics_for_vip_users()
    print(json.dumps(vip_metrics, indent=4))

if __name__ == '__main__':
    main()