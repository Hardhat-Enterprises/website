import requests
from django.conf import settings

# Function to check if an IP is blacklisted using VirusTotal
def check_ip_blacklist(ip_address):
    api_key = settings.VIRUSTOTAL_API_KEY
    url = 'https://www.virustotal.com/api/v3/ip_addresses/{ip_address}'

    headers = {
        'x-apikey': api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Check if the IP is flagged (you can refine this based on the structure of the response)
        if 'data' in data and 'attributes' in data['data']:
            ip_data = data['data']['attributes']
            if ip_data.get('last_analysis_stats', {}).get('malicious', 0) > 0:
                return True  # The IP is flagged as malicious
        return False
    else:
        # If the API call fails, return False
        return False
