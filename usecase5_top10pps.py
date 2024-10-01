import requests
import json

# Set up the Mist API credentials
# Use case5:- Top 10 Apps with maximum user associated Locatio wise Dashboard ..URL is not available.

MIST_API_KEY = 'xh9oBdbYQllXCmCh5Ad63h3Y3enrewPWrDD37XpYA5f1ealYTPJQEb2FMkmo0DBi9vFIiLJpNlHd6fM95Zog8e0NldKTnOol'
ORG_ID = '15e7597e-9b06-4381-8443-16aba95c5e0d'

# Define the headers for the API request
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Token {MIST_API_KEY}'
}

# Function to get application usage data
def get_application_usage(org_id):
    url = f"https://api.eu.mist.com/api/v1/orgs/{org_id}/insights/applications"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Function to process data and get top 10 applications per location
def process_application_data(data):
    location_data = {}
    for entry in data:
        location = entry['site_name']
        app_name = entry['app_name']
        users = entry['users']
        
        if location not in location_data:
            location_data[location] = []
        
        location_data[location].append({'app_name': app_name, 'users': users})
        
        # Sort and get top 10 applications
        location_data[location] = sorted(location_data[location], key=lambda x: x['users'], reverse=True)[:10]
    
    return location_data

# Fetch application usage data
data = get_application_usage(ORG_ID)

# Process and display top 10 applications per location
if data:
    top_apps_by_location = process_application_data(data)
    for location, apps in top_apps_by_location.items():
        print(f"Location: {location}")
        for app in apps:
            print(f"Application: {app['app_name']}, Users: {app['users']}")
        print("\n")
else:
    print("Failed to retrieve application usage data.")
