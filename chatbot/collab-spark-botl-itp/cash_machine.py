"""
Script para coleta de infromações sobre status das maquinas de pagamento
"""

import json
import requests


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
