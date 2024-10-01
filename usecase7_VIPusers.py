import requests
import json

# Define your Mist API credentials and organization/site IDs
# UseCase7:- Proactive monitoring of VIP users 

api_token = 'xh9oBdbYQllXCmCh5Ad63h3Y3enrewPWrDD37XpYA5f1ealYTPJQEb2FMkmo0DBi9vFIiLJpNlHd6fM95Zog8e0NldKTnOol'
org_id = '15e7597e-9b06-4381-8443-16aba95c5e0d'
site_id = '7ddd12b8-7ecf-451f-9f52-88b3b7ae30c3'

# Headers for the API requests
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Token {api_token}'
}

## Define the list of VIP user MAC addresses or user IDs
vip_users = ['2c:0d:a7:ca:43:ec', 'c4:03:a8:f3:97:29','70:1a:b8:53:44:e0','10:a5:1d:29:b5:49','c4:03:a8:f3:7b:3b','2C:0d:a7:c8:f2:0d','f4:26:79:b9:9b:dc']  # replace with actual MAC addresses or user IDs

def get_wifi_metrics_for_vip_users():
    vip_metrics = {}

    for user in vip_users:
        # Get the client's connection details
        response = requests.get(
            f'https://api.eu.mist.com/api/v1/sites/{site_id}/stats/clients?mac={user}',
            headers=headers
        )

        if response.status_code == 200:
            client_data = response.json()
            if client_data:
                client_info = client_data[0]  # Assuming the first entry is the relevant one
                vip_metrics[user] = {
                    'client_name': client_info.get('device_name', 'N/A'),
                    'mac_address': client_info.get('mac', 'N/A'),
                    'connected_ssid': client_info.get('ssid', 'N/A'),
                    'signal_strength': client_info.get('rssi', 'N/A'),
                    'data_usage': client_info.get('bytes_used', 'N/A'),
                    'last_seen': client_info.get('last_seen', 'N/A'),
                    'ip': client_info.get('ip', 'N/A'),
                    'uptime': client_info.get('uptime', 'N/A'),
                    'vlan_id': client_info.get('vlan_id', 'N/A'),
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