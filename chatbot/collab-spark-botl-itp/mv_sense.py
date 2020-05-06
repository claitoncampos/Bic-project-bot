"""
Script para capturar o número de pessoas em uma determinada zona da câmera MV
"""

import requests
import json
from datetime import datetime

# Live API
print('Pessoas detectadas')
today = datetime.now()
meraki_live_url = 'https://api.meraki.com/api/v0/devices/Q2EV-ALRC-2U8N/camera/analytics/live'
meraki_headers = {'X-Cisco-Meraki-API-Key': 'da098b591db185af6c82845188ded2e8728dfe30'}
meraki_live_response = requests.get(meraki_live_url, headers=meraki_headers)
meraki_live_response_json = json.loads(meraki_live_response.text)
num_of_person_detected = meraki_live_response_json['zones']['635570497412661529']

print(today, num_of_person_detected)


print('zoneId')
meraki_live_url = 'https://api.meraki.com/api/v0/devices/Q2EV-ALRC-2U8N/camera/analytics/zones'
meraki_headers = {'X-Cisco-Meraki-API-Key': 'da098b591db185af6c82845188ded2e8728dfe30'}
meraki_live_response = requests.get(meraki_live_url, headers=meraki_headers)
meraki_live_response_json = json.loads(meraki_live_response.text)
zoneId = meraki_live_response_json

#for zone in zoneId:
#    if zone['zoneId'] == '635570497412661529':
#        print('PDV')
#    elif zone['zoneId'] == '635570497412661530':
#        print('Porta Principal')

print(zoneId)
