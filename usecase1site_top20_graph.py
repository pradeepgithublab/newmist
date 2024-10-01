import json
import requests
import matplotlib.pyplot as plt

# configuration variables
api_token = 'xh9oBdbYQllXCmCh5Ad63h3Y3enrewPWrDD37XpYA5f1ealYTPJQEb2FMkmo0DBi9vFIiLJpNlHd6fM95Zog8e0NldKTnOol'
base_url = 'https://api.eu.mist.com/api/v1'
site_id = 'a631d811-8b9b-48ef-823b-b5594e4af356'
limit = 20
total_records = 20

def get_client_data():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {api_token}',
    }
    offset = 0
    clients = []

    # Fetch data in chunks of 'limit' until 'total_records' is reached
    while len(clients) < total_records:
        try:
            response = requests.get(
                f'{base_url}/sites/{site_id}/insights/top-client',
                headers=headers,
                params={'limit': limit, 'offset': offset}
            )

            # Check if the response is valid
            if response.status_code != 200:
                print(f"Error: Received status code {response.status_code}")
                break

            try:
                clients_batch = response.json().get('results', [])
            except requests.exceptions.JSONDecodeError as e:
                print(f"JSON decode error: {e.msg}")
                print(f"Response text: {response.text}")
                break

            if not clients_batch:
                # No more data available
                break

            clients.extend(clients_batch)
            offset += limit

        except requests.RequestException as e:
            print(f"Request error: {e}")
            break

    return clients

# Function to process client data
def process_client_data(clients):
    data = []
    initial_value = 0
    for client in clients:
        data.append({
            'mac': client.get('mac'),
            'site': client.get('site'),
            'total_bytes': client.get('total_bytes'),
        })
        initial_value += 1
        if initial_value >= limit:
            break
    return data

def plot_client_data(client_data):
    # Sort the client data by total_bytes in descending order
    client_data.sort(key=lambda x: x['total_bytes'], reverse=True)

    # Extract MAC addresses and total bytes for plotting
    mac_addresses = [client['mac'] for client in client_data]
    total_bytes = [client['total_bytes'] for client in client_data]

    # Create the bar chart
    plt.figure(figsize=(12, 8))
    plt.barh(mac_addresses, total_bytes, color='skyblue')
    plt.xlabel('Total Bytes')
    plt.ylabel('MAC Address')
    plt.title('Top 20 Users by Bandwidth Consumption')
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest value on top
    plt.tight_layout()
    plt.show()

def main():
    # Retrieve client data from the API
    clients = get_client_data()

    # Process the retrieved client data
    client_data = process_client_data(clients)

    # Plot the processed data
    plot_client_data(client_data)

if __name__ == "__main__":
    main()
