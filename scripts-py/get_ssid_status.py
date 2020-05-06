import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Acessando a API Key no arquivo .env
api_key = os.getenv('MERAKI_DASHBOARD_API_KEY')

# Base url para as APIs Meraki
base_url = 'https://api.meraki.com/api/v0/'

# Header com a chave para acessar as APIs
headers = {'X-Cisco-Meraki-API-Key': api_key}

# Funcao para coletar o status da rede wi-fi (ativa ou nao)
def get_ssid_status():
    api = base_url + 'networks/L_635570497412679069/devices/Q2GD-5BHC-UAL2/wireless/status'
    r = requests.get(api, headers=headers)
    json_data = r.json()
    org_id = json_data['basicServiceSets'][0]['enabled']
    return org_id


print('rede habilitada:', get_ssid_status())
