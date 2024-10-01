import json
import requests

# configuration variables
api_token = 'xh9oBdbYQllXCmCh5Ad63h3Y3enrewPWrDD37XpYA5f1ealYTPJQEb2FMkmo0DBi9vFIiLJpNlHd6fM95Zog8e0NldKTnOol'
base_url = 'https://api.eu.mist.com/api/v1'
org_id = '15e7597e-9b06-4381-8443-16aba95c5e0d'
site_id = 'a631d811-8b9b-48ef-823b-b5594e4af356'
limit = 20

def get_client_data():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {api_token}',
    }
    offset = 0
    clients = []

    # Fetch data in chunks of 'limit' until 'total_records' is reached
    while len(clients) < limit:
        try:
            response = requests.get(
                f'{base_url}/orgs/{org_id}/sites/{site_id}/insights/top-client',
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
    for client in clients:
        data.append({
            'mac': client.get('mac'),
            'site': client.get('site'),
            'total_bytes': client.get('total_bytes'),
        })
        if len(data) >= limit:
            break
    return data

def main():
    # Retrieve client data from the API
    clients = get_client_data()

    # Process the retrieved client data
    client_data = process_client_data(clients)

    # Print processed data
    for item in client_data:
        print(item)

if __name__ == "__main__":
    main()
