import requests
import matplotlib.pyplot as plt
import numpy as np

# Replace with your Juniper Mist API credentials and endpoint
api_token = 'xh9oBdbYQllXCmCh5Ad63h3Y3enrewPWrDD37XpYA5f1ealYTPJQEb2FMkmo0DBi9vFIiLJpNlHd6fM95Zog8e0NldKTnOol'
org_id = '15e7597e-9b06-4381-8443-16aba95c5e0d'
base_url = 'https://api.eu.mist.com/api/v1'

# Function to get APs data
def get_aps_data():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {api_token}',
    }
    response = requests.get(f'{base_url}/orgs/{org_id}/sites', headers=headers)
    sites = response.json()
    
    ap_data = []
    for site in sites:
        site_id = site['id']
        site_name = site['name']
        response = requests.get(f'{base_url}/sites/{site_id}/stats/devices', headers=headers)
        devices = response.json()
        connected = len([ap for ap in devices if ap['status'] == 'connected'])
        disconnected = len([ap for ap in devices if ap['status'] == 'disconnected'])
        ap_data.append((site_name, connected, disconnected))
    
    return ap_data

# Function to plot data
def plot_aps_data(ap_data):
    locations = [data[0] for data in ap_data]
    connected = [data[1] for data in ap_data]
    disconnected = [data[2] for data in ap_data]

    bar_width = 0.35
    index = np.arange(len(locations))

    fig, ax = plt.subplots()
    bar1 = plt.bar(index, connected, bar_width, label='Connected')
    bar2 = plt.bar(index + bar_width, disconnected, bar_width, label='Disconnected')

    plt.xlabel('Location')
    plt.ylabel('Count of APs')
    plt.title('Connected and Disconnected APs by Location')
    plt.xticks(index + bar_width / 2, locations, rotation=45)
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    ap_data = get_aps_data()
    plot_aps_data(ap_data)
