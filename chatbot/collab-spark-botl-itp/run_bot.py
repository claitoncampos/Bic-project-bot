from pprint import pprint
import requests
import json
import sys
import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime



dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


try:
    from flask import Flask
    from flask import request
except ImportError as e:
    print(e)
    print("Looks like 'flask' library is missing.\n"
          "Type 'pip3 install flask' command to install the missing library.")
    sys.exit()


# BOT'S ACCESS TOKEN
bearer = os.environ.get("TEAMS_ACCESS_TOKEN")
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Bearer " + bearer
}


expected_messages = {"help me": "help",
                     "need help": "help",
                     "can you help me": "help",
                     "ayuda me": "help",
                     "help": "help",
                     "greetings": "greetings",
                     "hello": "greetings",
                     "hi": "greetings",
                     "how are you": "greetings",
                     "what's up": "greetings",
                     "sam": "sam",
                     "status": "summary",
                     "loja": "store",
                     "1": "networkstatus",
                     "2": "env_temperature",
                     "3": "get_snapshot",
                     "falha": "device_status_detail",
                     "rede": "networkstatus",
                     "clientes": "user_logged_wifi",
                     "temperatura": "env_temperature",
                     "ativar": "enable_guest_wifi",
                     "foto": "get_snapshot",
                     "fila": "mv_sense",
                     "pos": "cashmachine",
                     "chamados": "tickets",
                     "what's up doc": "greetings"

                     }


def send_get(url, payload=None,js=True):

    if payload == None:
        request = requests.get(url, headers=headers)
    else:
        request = requests.get(url, headers=headers, params=payload)
    if js == True:
        request= request.json()
    return request


def send_post(url, data):

    request = requests.post(url, json.dumps(data), headers=headers).json()
    return request


def help_me():

    return "Sure! I can help. Below are the commands that I understand:<br/>" \
           "`Help me` - I will display what I can do.<br/>" \
           "`Hello` - I will display my greeting message<br/>" \
           "`Repeat after me` - I will repeat after you <br/>"


def greetings():

    return "Hi my name is %s.<br/>" \
           "Type `Help me` to see what I can do.<br/>" % bot_name


def summary():

    # Funcao para informar a data e hora atual
    today = datetime.now()

    return "Bom dia, segue a situação atual da loja para a data do dia" + ' ' + str(today) + ' ' + "<br/>" \
            "<br/>" \
            "A temperatura atual no interior da loja é de" + ' ' + env_temperature() + ' ' "<br/>" \
            "<br/>" \
           "No momento" + ' ' + get_organization_device_statuses() + "<br/>" \
           "<br/>" \
           "Atualmente no help desk," + ' ' + tickets() + "<br/>" \
           "<br/>" \
           "Na rede wi-fi" + ' ' + user_logged_wifi() + "<br/>" \
           "<br/>" \
           "No momento," + ' ' + mv_sense() + ' ' + "<br/>" \
           "<br/>" \
           "Sempre que precisar de alguma informação adicional você pode me solicitar digitando a palavra **Loja**"


def sam():

    return "Ola, eu sou o S.A.M, seu assistente pessoal <br/>" \
           "Voce pode a qualquer momento solicitar informacoes <br/>" \
           "sobre sua loja, para isso basta você escrever (loja) <br/>" \
           "e lhe apresentarei algumas possibilidades de interação."


def store():

    return "O que voce gostaria de verificar?<br/>" \
            "**1)** Verificar o status da rede wi-fi: (**rede**)<br/>" \
            "**2)** Verificar a quantidade de pessoas na rede wifi: (**clientes**)<br/>"\
            "**3)** Verificar a temperatura do ar condicionado na loja: (**temperatura**)<br/>" \
            "**4)** Para receber um snapshot da camera: (**foto**)<br/>" \
            "**5)** Verificar o status de toda a rede (saude da rede): (**falha**)<br/>" \
            "**6)** Saber o numero de pessoas na fila aguardando atendimento: (**fila**)<br/>" \
            "**7)** Verificar o numero de chamados abertos no Suporte: (**chamados**)<br/>" \
            "**8)** Ter o status dos sistemas de pagamento (online ou offline): (**pos**)<br/>"\
            "**9)** Verificar o status da operacao da loja: (**status**)<br/>"\



# Funcao para coletar a informação de status da rede wi-fi (on ou off)
def networkstatus():

    # Acessando a API Key no arquivo .env
    api_key = os.getenv('MERAKI_DASHBOARD_API_KEY')
    # Base url para as APIs Meraki
    base_url = 'https://api.meraki.com/api/v0/'
    # Header com a chave para acessar as APIs
    headers_meraki = {'X-Cisco-Meraki-API-Key': api_key}
    api = base_url + 'networks/L_635570497412679069/devices/Q2GD-5BHC-UAL2/wireless/status'
    r = requests.get(api, headers=headers_meraki)
    json_data = r.json()
    org_id = json_data['basicServiceSets'][0]['enabled']
    if org_id == True:
        return "Rede BIC-GUEST esta operando normalmente"
    else:
        return "Rede BIC-GUEST esta desativada no momento<br/>"\
               "Gostaria de ativar a rede?<br/>" \
               "Para ativar digite a palavra (**ativar**)"


def env_temperature():
    """
    Script para leitura de temperatura através do sensor da SMETRO
    Leitura realizada através de consulta do endpoint que serve o dashboard com as informações de temperatura
    O endpoit registra as últimas 12 temperaturas a cada 30 minutos.
    """

    url = 'https://y5s4g14t3k.execute-api.us-east-1.amazonaws.com/development/temperatures'

    response = requests.request("GET", url)
    temperatures = json.loads(response.text.encode('utf8'))['temperatures']
    temperature = json.loads(temperatures)[0]['temperature']
    data = temperature[0]['data']

    if data <= 24.99:
        return str(data) + ' ' + "graus, esta muito agradavel para nossos clientes"
    elif data >= 25.00:
        return str(data) + ' ' + "graus, esta acima do ideal!"


def get_organization_device_statuses():

    # Acessando a API Key no arquivo .env
    api_key = os.getenv('MERAKI_DASHBOARD_API_KEY')
    # Base url para as APIs Meraki
    url = "https://api.meraki.com/api/v0/organizations/945091/deviceStatuses"
    payload = '{}'
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Cisco-Meraki-API-Key': api_key
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    device_status = json.loads(response.text.encode('utf8'))

    i = 0
    for status in device_status:
        if status['status'] == 'offline':
            i += 1
    if i == 0:
        return 'todos os ativos de rede estão funcionando normalmente'
    elif i == 1:
        return 'foi identificado que' + ' ' + str(i) + ' ' + 'equipamento esta offline'
    elif i >= 2:
        return 'foram identificados que' + ' ' + str(i) + ' ' + 'equipamentos estao offline'


def device_status_detail():

    # Acessando a API Key no arquivo .env
    api_key = os.getenv('MERAKI_DASHBOARD_API_KEY')
    # Base url para as APIs Meraki
    url = "https://api.meraki.com/api/v0/organizations/945091/deviceStatuses"
    payload = '{}'
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Cisco-Meraki-API-Key': api_key
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    device_status = json.loads(response.text.encode('utf8'))

    #FIXME: Tive que fazer uma gambiarra usando lista, ficou ruim mas funciona
    my_list = []
    for status in device_status:
        if status['status'] == 'offline':
            my_list.append(status['name'] + ' ' + 'esta offline' + ' ' + 'desde' + ' ' + status['lastReportedAt'])

    return str(my_list)


# Funcao para habilitar a rede wireless através do BOT
def enable_guest_wifi():

    # Acessando a API Key no arquivo .env
    api_key = os.getenv('MERAKI_DASHBOARD_API_KEY')
    # Base url para as APIs Meraki
    base_url = 'https://api.meraki.com/api/v0/'
    url = base_url + 'networks/L_635570497412679069/ssids/0'
    payload = 'enabled=True'
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Cisco-Meraki-API-Key': api_key
    }
    response = requests.put(url, data=payload, headers=headers)
    json_name = response.json()['name']
    json_status = response.json()['enabled']
    if json_status == True:
        return 'Rede' + " " + json_name + " " + 'habilitada'
    else:
        return ('Humm, parece que houve um problema para ativar a rede')


# Funcao para receber snapshot da camera Meraki
def get_snapshot():

    # Acessando a API Key no arquivo .env
    api_key = os.getenv('MERAKI_DASHBOARD_API_KEY')

    # url para snapshot da camera Meraki
    url = 'https://api.meraki.com/api/v0/networks/L_635570497412679069/cameras/Q2EV-ALRC-2U8N/snapshot'
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Cisco-Meraki-API-Key': api_key
    }
    payload = "{}"
    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = response.json()
    url_snapshot = json_data['url']
    #snapshot = requests.request("GET", url_snapshot)
    return 'Clique na URL abaixo para poder verificar o snapshot atual da camera<br/>' + '<br/>' + url_snapshot


def mv_sense():
    """
    Funcao para capturar o número de pessoas em uma determinada zona da câmera MV
    """

    try:

        api_key = os.getenv('MERAKI_DASHBOARD_API_KEY')
        meraki_live_url = 'https://api.meraki.com/api/v0/devices/Q2EV-ALRC-2U8N/camera/analytics/live'
        meraki_headers = {'X-Cisco-Meraki-API-Key': api_key}
        meraki_live_response = requests.get(meraki_live_url, headers=meraki_headers)
        meraki_live_response_json = json.loads(meraki_live_response.text)
        num_of_person_detected = meraki_live_response_json['zones']['635570497412661529']['person']

        if num_of_person_detected == 0:
            return 'não existem pessoas aguardando atendimento na fila do caixa'
        else:
            return 'a quantidade de pessoas aguardando atendimento na fila do caixa eh de: ' + '' + str(num_of_person_detected)

    except:
        return 'estes dados estao inacessiveis'


def tickets():
    """
    Funcao para retornar a quantidade de tickets abertos na plataforma Freshdesk
    """
    url = "https://suportebic.freshdesk.com/api/v2/search/tickets?query=\"status:2\""

    payload = {}
    headers = {
        'apikey': 'aTTvEg83633jwShbEUhj',
        'Authorization': 'Basic YVRUdkVnODM2MzNqd1NoYkVVaGo6eA==',
        'Cookie': '_x_w=37_2; _x_m=x_c'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    total_tickets = json.loads(response.text.encode('utf8'))['total']

    if total_tickets == 0:
        return 'nao existem tickets abertos.'
    elif total_tickets == 1:
        return 'existe apenas ' + str(total_tickets) + ' ' + 'ticket aberto e aguardando atendimento.'
    elif total_tickets >= 2:
        return 'existem um total de ' + str(total_tickets) + ' ' + 'tickets abertos e aguardando atendimento.'


def cashmachine():

    def maquina_cartao_status():

        try:

            # url para coleta de informacao de status da Maquina de cartao
            url = 'https://y5s4g14t3k.execute-api.us-east-1.amazonaws.com/development/ccm'

            response = requests.request('GET', url)
            ccm_status = json.loads(response.text.encode('utf8'))

            for status in ccm_status['ccm']:
                if status['status'] == 'on':
                    return 'Sistema de pagamento via maquina de cartao esta operacional'

                else:
                    return 'Maquina de cartao esta desligada'
        except:
            return 'Sem informacoes no momento'

    def pdv():

        try:

            # url para coleta de informacoes de status do PDV
            url = 'https://y5s4g14t3k.execute-api.us-east-1.amazonaws.com/development/pos'

            response = requests.request('GET', url)
            pdv_status = json.loads(response.text.encode('utf8'))

            for status in pdv_status['pdv']:
                if status['status'] == 'on':
                    return 'Sistema de pagamento POS esta operacional'
                else:
                    return 'PDV esta desligado'
        except:
            return 'Sem informacoes no momento'

    return maquina_cartao_status() + ',' + ' ' + pdv()


def user_logged_wifi():

    url = "https://api.meraki.com/api/v0/networks/L_635570497412679069/clients"
    api_key = os.getenv('MERAKI_DASHBOARD_API_KEY')
    payload = {}
    headers = {
        'Accept': '*/*',
        'X-Cisco-Meraki-API-Key': api_key
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    user_detail = json.loads(response.text.encode('utf8'))
    user_connection_status = user_detail

    i = 0
    for status in user_connection_status:
        if status['status'] == 'Online':
            i += 1
    if i == 0:
        return 'nao ha ninguem conectado'

    elif i == 1:
        return 'temos atualmente' + ' ' + str(i) + ' ' + 'cliente conectado'

    elif i >= 2:
        return 'temos atualmente' + ' ' + str(i) + ' ' + 'clientes conectados'



app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def teams_webhook():
    if request.method == 'POST':
        webhook = request.get_json(silent=True)
        if webhook['data']['personEmail']!= bot_email:
            pprint(webhook)
        if webhook['resource'] == "memberships" and webhook['data']['personEmail'] == bot_email:
            send_post("https://api.ciscospark.com/v1/messages",
                            {
                                "roomId": webhook['data']['roomId'],
                                "markdown": (greetings() +
                                             "**Note This is a group room and you have to call "
                                             "me specifically with `@%s` for me to respond**" % bot_name)
                            }
                            )
        msg = None
        if "@webex.bot" not in webhook['data']['personEmail']:
            result = send_get(
                'https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
            in_message = result.get('text', '').lower()
            in_message = in_message.replace(bot_name.lower() + " ", '')
            if in_message.startswith('help me'):
                msg = help_me()
            elif in_message.startswith('hello'):
                msg = greetings()
            elif in_message.startswith('sam'):
                msg = sam()
            elif in_message.startswith('status'):
                msg = summary()
            elif in_message.startswith('loja'):
                msg = store()
            elif in_message.startswith('1'):
                msg = networkstatus()
            elif in_message.startswith('rede'):
                msg = networkstatus()
            elif in_message.startswith('clientes'):
                msg = user_logged_wifi()
            elif in_message.startswith('ativar'):
                msg = enable_guest_wifi()
            elif in_message.startswith('temperatura'):
                msg = env_temperature()
            elif in_message.startswith('foto'):
                msg = get_snapshot()
            elif in_message.startswith('falha'):
                msg = device_status_detail()
            elif in_message.startswith('fila'):
                msg = mv_sense()
            elif in_message.startswith('chamados'):
                msg = tickets()
            elif in_message.startswith('pos'):
                msg = cashmachine()
            elif in_message.startswith("repeat after me"):
                message = in_message.split('repeat after me ')[1]
                if len(message) > 0:
                    msg = "{0}".format(message)
                else:
                    msg = "I did not get that. Sorry!"
            else:
                msg = "Sorry, but I did not understand your request. Type `Help me` to see what I can do"
            if msg != None:
                send_post("https://api.ciscospark.com/v1/messages",
                                {"roomId": webhook['data']['roomId'], "markdown": msg})
        return "true"
    elif request.method == 'GET':
        message = "<center><img src=\"https://cdn-images-1.medium.com/max/800/1*wrYQF1qZ3GePyrVn-Sp0UQ.png\" alt=\"Webex Teams Bot\" style=\"width:256; height:256;\"</center>" \
                  "<center><h2><b>Congratulations! Your <i style=\"color:#ff8000;\">%s</i> bot is up and running.</b></h2></center>" \
                  "<center><b><i>Don't forget to create Webhooks to start receiving events from Webex Teams!</i></b></center>" % bot_name
        return message

def main():
    global bot_email, bot_name
    if len(bearer) != 0:
        test_auth = send_get("https://api.ciscospark.com/v1/people/me", js=False)
        if test_auth.status_code == 401:
            print("Looks like the provided access token is not correct.\n"
                  "Please review it and make sure it belongs to your bot account.\n"
                  "Do not worry if you have lost the access token. "
                  "You can always go to https://developer.webex.com/my-apps "
                  "and generate a new access token.")
            sys.exit()
        if test_auth.status_code == 200:
            test_auth = test_auth.json()
            bot_name = test_auth.get("displayName","")
            bot_email = test_auth.get("emails","")[0]
    else:
        print("'bearer' variable is empty! \n"
              "Please populate it with bot's access token and run the script again.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.webex.com/my-apps "
              "and generate a new access token.")
        sys.exit()

    if "@webex.bot" not in bot_email:
        print("You have provided an access token which does not relate to a Bot Account.\n"
              "Please change for a Bot Account access token, view it and make sure it belongs to your bot account.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.webex.com/my-apps "
              "and generate a new access token for your Bot.")
        sys.exit()
    else:
        app.run(host='localhost', port=8080)

if __name__ == "__main__":
    main()