import requests

# Replace with your Mist API credentials
# Use Case2:- List of AP's having some issues.

MIST_API_TOKEN = 'xh9oBdbYQllXCmCh5Ad63h3Y3enrewPWrDD37XpYA5f1ealYTPJQEb2FMkmo0DBi9vFIiLJpNlHd6fM95Zog8e0NldKTnOol'
ORG_ID = '15e7597e-9b06-4381-8443-16aba95c5e0d'
SITE_ID = 'a631d811-8b9b-48ef-823b-b5594e4af356'

def get_unhealthy_aps():
    headers = {
        'Authorization': f'Token {MIST_API_TOKEN}'
    }
    url = f'https://api.eu.mist.com/api/v1/sites/{SITE_ID}/stats/devices'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        devices = response.json()
        unhealthy_aps = [device for device in devices if device.get('type') == 'ap' and device.get('usage', 0) < 50]
        
        for ap in unhealthy_aps:
            print(f"AP MAC: {ap.get('mac')}, Utilization: {ap.get('cpu_util')}%, Name: {ap.get('name')}, Model: {ap.get('model')}")
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    get_unhealthy_aps()

