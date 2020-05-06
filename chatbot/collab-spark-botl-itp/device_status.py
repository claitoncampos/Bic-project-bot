"""

"""

import json
import requests

url = "https://api.meraki.com/api/v0/organizations/945091/deviceStatuses"

payload = {}
headers = {
  'Accept': '*/*',
  'X-Cisco-Meraki-API-Key': 'da098b591db185af6c82845188ded2e8728dfe30'
}

response = requests.request("GET", url, headers=headers, data=payload)
device_status = json.loads(response.text.encode('utf8'))


for status in device_status:
    if status['status'] == 'offline':
        print(status['name'] + ' ' + 'esta offline' + ' ' + 'desde' + ' ' + status['lastReportedAt'])
    elif status['status'] == 'online':
        print('Todos os equipamentos estao operacionais')
