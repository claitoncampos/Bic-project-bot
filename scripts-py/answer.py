import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
import urllib.request
import json

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Acessando a API Key no arquivo .env
bearer = os.getenv('TEAMS_BOT_TOKEN')
url = 'https://envoct8zyyc1m.x.pipedream.net/'
headers = {"Accept": "application/json", "Content-Type":"application/json", }

def sendSparkGET():
    request = requests.get(url, headers=headers)
    request.add_header("Authorization", "Bearer "+bearer)
    json_data = request.json()
    contents = json_data
    return contents

@post('/')
def index(request):
    webhook = json.loads(request.body)
    #print webhook['data']['id']
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)
    #print result
    if 'teste' in result.get('text', '').lower():
        print ("Teste ok")
    elif 'test' in result.get('text', '').lower():
        print ("The test")
    elif 'testee' in result.get('text', '').lower():
        print( "ok ok")
    return "true"

def sendSparkPOST(url, data):
    request = requests.post(url, json.dumps(data),
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib.request.urlopen(request).read()
    return contents

@post('/')
def index(request):
    webhook = json.loads(request.body)
    print (webhook['data']['id'])
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)
    msg = None
    if webhook['data']['personEmail'] != bot_email:
        in_message = result.get('text', '').lower()
        in_message = in in_message.replace(bot_name, '')
        if 'teste' in in_message or "whoareyou" in in_message:
            msg = "I'm Batman!"
        elif 'test' in in_message:
            message = result.get('text').split('batcave')[1].strip(" ")
            if len(message) > 0:
                msg = "The Batcave echoes, '{0}'".format(message)
            else:
                msg = "The Batcave is silent..."
        elif 'batsignal' in in_message:
            print ("NANA NANA NANA NANA")
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data'][
                'roomId'], "files": bat_signal})
            if msg != None:
                print msg
                sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data'][
                    'roomId'], "text": msg})
                return "true"

print(sendSparkGET())
