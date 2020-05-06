"""
Script para leitura de temperatura através do sensor da SMETRO
Leitura realizada através de consulta do endpoint que serve o dashboard com as informações de temperatura
O endpoit registra as últimas 12 temperaturas a cada 30 minutos.
"""

import json
import requests

url = 'https://y5s4g14t3k.execute-api.us-east-1.amazonaws.com/development/temperatures'


response = requests.request("GET", url)
temperatures = json.loads(response.text)['temperatures']
temperature = json.loads(temperatures)[0]['temperature']
data = temperature[0]['data']
env_temp = data

if data <= 24.99:
    print("A temperatura esta agradavel")
elif data >= 25.00:
    print("A temperatura esta alta")

print('A temperatura atual na loja é de', env_temp, 'graus')
print(type(env_temp))
