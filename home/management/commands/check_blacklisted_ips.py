def check_ip_blacklist(ip_address):
    print("Checking IP: {ip_address}")  # Debugging line

    api_key = settings.VIRUSTOTAL_API_KEY
    url = 'https://www.virustotal.com/api/v3/ip_addresses/{ip_address}'

    headers = {
        'x-apikey': api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("API response:", data)  # Debugging line

        if 'data' in data and 'attributes' in data['data']:
            ip_data = data['data']['attributes']
            malicious_count = ip_data.get('last_analysis_stats', {}).get('malicious', 0)

            if malicious_count > 0:
                print(f"IP {ip_address} is flagged as malicious.")  # Debugging line
                return True
        return False
    else:
        print(f"Error with API call. Status code: {response.status_code}")  # Debugging line
        return False
