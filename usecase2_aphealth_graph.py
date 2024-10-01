import requests
import matplotlib.pyplot as plt

# Replace with your Mist API credentials
MIST_API_TOKEN = 'xh9oBdbYQllXCmCh5Ad63h3Y3enrewPWrDD37XpYA5f1ealYTPJQEb2FMkmo0DBi9vFIiLJpNlHd6fM95Zog8e0NldKTnOol'
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
        return unhealthy_aps
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []

def plot_unhealthy_aps(unhealthy_aps):
    # Extracting data for plotting
    ap_names = [ap.get('name', 'Unknown') for ap in unhealthy_aps]
    utilizations = [ap.get('cpu_util', 0) for ap in unhealthy_aps]

    # Creating the bar chart
    plt.figure(figsize=(12, 8))
    plt.barh(ap_names, utilizations, color='salmon')
    plt.xlabel('CPU Utilization (%)')
    plt.ylabel('Access Point Name')
    plt.title('Unhealthy APs by CPU Utilization')
    plt.gca().invert_yaxis()  # Highest utilization on top
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    unhealthy_aps = get_unhealthy_aps()
    if unhealthy_aps:
        plot_unhealthy_aps(unhealthy_aps)
