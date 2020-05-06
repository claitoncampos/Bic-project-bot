"""
Script para coleta de informações sobre tickets abertos/ resolvidos na plataforma Freshdesk
"""


import json
import requests

url = "https://suportebic.freshdesk.com/api/v2/search/tickets?query=\"status:2\""

payload = {}
headers = {
  'apikey': 'aTTvEg83633jwShbEUhj',
  'Authorization': 'Basic YVRUdkVnODM2MzNqd1NoYkVVaGo6eA==',
  'Cookie': '_x_w=37_2; _x_m=x_c'
}

response = requests.request("GET", url, headers=headers, data=payload)
total_tickets = json.loads(response.text.encode('utf8'))['total']

print(total_tickets)

if total_tickets == 0:
    print('nao existem tickets abertos')
elif total_tickets >= 1:
    print('existem um total de ' + str(total_tickets) + ' ' + 'tickets aguardando atendimento')

print(total_tickets)
