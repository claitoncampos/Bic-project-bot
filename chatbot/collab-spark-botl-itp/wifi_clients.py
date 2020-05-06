"""
Script para coleta de informações do número de clientes conectados na rede wi-fi
"""

import json
import requests


url = "https://api.meraki.com/api/v0/networks/L_635570497412679069/clients"

payload = {}
headers = {
  'Accept': '*/*',
  'X-Cisco-Meraki-API-Key': 'da098b591db185af6c82845188ded2e8728dfe30'
}

response = requests.request("GET", url, headers=headers, data=payload)
user_detail = json.loads(response.text.encode('utf8'))
user_connection_status = user_detail


i = 0
for status in user_connection_status:
    if status['status'] == 'Online':
        i += 1

        if i == '[]':
            print('nao ha ninguem conectado')

        elif i == 0:
            print('nao ha ninguem conectado')

        elif i == 1:
            print('existe' + ' ' + str(i) + ' ' + 'cliente conectado')

        elif i >= 2:
            print('existem' + ' ' + str(i) + ' ' + 'clientes conectados')
