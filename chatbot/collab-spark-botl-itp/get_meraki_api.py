import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
from io import BytesIO
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Acessando a API Key no arquivo .env
api_key = os.getenv('MERAKI_DASHBOARD_API_KEY')

# Base url para as APIs Meraki
base_url = 'https://api.meraki.com/api/v0/'

# Header com a chave para acessar as APIs
headers_meraki = {'X-Cisco-Meraki-API-Key': api_key,
                  'Accept': '*/*',
                  'Content-Type': 'application/json'
                  }
payload = "{}"
# Funcao para coletar o status da rede wi-fi (ativa ou nao)
#def get_ssid_status():
#
#    # Acessando a API Key no arquivo .env
#    api_key = os.getenv('MERAKI_DASHBOARD_API_KEY')
#    # Base url para as APIs Meraki
#    base_url = 'https://api.meraki.com/api/v0/'
#    url = base_url + 'networks/L_635570497412679069/ssids/0'
#    payload = 'enabled=True'
#    headers = {
#        'Accept': '*/*',
#        'Content-Type': 'application/x-www-form-urlencoded',
#        'X-Cisco-Meraki-API-Key': api_key
#    }
#    response = requests.put(url, data=payload, headers=headers)
#    json_name = response.json()['name']
#    json_status = response.json()['enabled']
#    if json_status == True:
#        return 'Rede' + " " + json_name + " "+ 'habilitada'
#    else:
#        return ('Problemas para ativar')


#print(get_ssid_status())

def mv_sense():
    """
    Script para capturar o número de pessoas em uma determinada zona da câmera MV
    """
    api_key = os.getenv('MERAKI_DASHBOARD_API_KEY')
    meraki_live_url = 'https://api.meraki.com/api/v0/devices/Q2EV-ALRC-2U8N/camera/analytics/live'
    meraki_headers = {'X-Cisco-Meraki-API-Key': api_key}
    meraki_live_response = requests.get(meraki_live_url, headers=meraki_headers)
    meraki_live_response_json = json.loads(meraki_live_response.text)
    num_of_person_detected = meraki_live_response_json['zones']['0']['person']

    return num_of_person_detected

print(mv_sense())

#def get_organization_device_statuses():
#
#    # Acessando a API Key no arquivo .env
#    api_key = os.getenv('MERAKI_DASHBOARD_API_KEY')
#    # Base url para as APIs Meraki
#    url = "https://api.meraki.com/api/v0/organizations/945091/deviceStatuses"
#    payload = '{}'
#    headers = {
#        'Accept': '*/*',
#        'Content-Type': 'application/x-www-form-urlencoded',
#        'X-Cisco-Meraki-API-Key': api_key
#    }
#    response = requests.request("GET", url, headers=headers, data=payload)
#    response_string = response.text.encode('utf8')
#    json_object = json.loads(response_string)
#
#
#    parse = json_object
#
#
#
#    for device in parse:
#
#        if device['status'] == 'offline':
#            a = 'O equipamento' + ' ' + device['name'] + ' ' + 'esta desconectado'
#
#            return a
#




#        status.append(device['name'] + ' ' + device['status'])
#        alarm.append(device['status'])







#       if alarm[i] == 'offline':
#           return 'Humm, parace que o' + ' ' + i['name'] + ' ' + 'esta desconectado'
#       else:
#           return 'Toda a rede esta operando normalmente'




#print(get_organization_device_statuses())



#def get_snapshot():
#
#    # Acessando a API Key no arquivo .env
#    api_key = os.getenv('MERAKI_DASHBOARD_API_KEY')
#    # url para snapshot da camera Meraki
#    url = 'https://api.meraki.com/api/v0/networks/L_635570497412679069/cameras/Q2EV-ALRC-2U8N/snapshot'
#    headers = {
#        'Accept': '*/*',
#        'Content-Type': 'application/x-www-form-urlencoded',
#        'X-Cisco-Meraki-API-Key': api_key
#    }
#    payload = "{}"
#    response = requests.request("POST", url, headers=headers, data=payload)
#    json_data = response.json()
#    url_snapshot = json_data['url']
##    return url_snapshot
#    # Captura a imagem pela URL
##    r = requests.get(url_snapshot)
##    return r
#    image = Image.open(BytesIO(url_snapshot))
#
#    path = "./image" + image.format
#
#    try:
#        image.save(path, image.format)
#    except IOError:
#        return ("Cannot save image")


