import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Acessando a API Key no arquivo .env
api_key = os.getenv('MERAKI_DASHBOARD_API_KEY')

# Define initial URL and headers
url = 'https://api.meraki.com/api/v0/'
headers = {
   'X-Cisco-Meraki-API-Key': api_key
}

# Create requests object using the URL and headers
api = url + 'networks/L_635570497412679069/devices/Q2GD-5BHC-UAL2/wireless/status'
r = requests.get(api, headers=headers)

# Assign the response to a variable in JSON format
json_data = r.json()

# Assign the organization ID to a variable and print
org_id = json_data['basicServiceSets'][0]['enabled']
print('rede habiltada:', org_id)
