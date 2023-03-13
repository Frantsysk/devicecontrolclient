import uuid
import platform
import configparser
import requests
import json
import psutil
from time import sleep

config = configparser.ConfigParser()

config.read('config.cfg')


def get_serial():
    """
    function that returns unique serial id of the device
    """
    return uuid.getnode()


def get_system():
    """
    function that returns os of the device
    """
    return platform.system()


def register_system():
    u_id = config.get('MAIN', 'id')
    if u_id == '':
        response = requests.post(url=config.get('MAIN', 'HOST') + '/register',
                   data=json.dumps({"account": "test777@gmail.com", "serial": get_serial(), "os": get_system()})).json()
        print(response)
        config.set('MAIN', 'id', str(response['id']))
        with open('config.cfg', 'w') as conf:
            config.write(conf)


def get_cpu_load():
    return psutil.cpu_percent(1)


def memory_usage():
    return psutil.virtual_memory().percent


def disk_usage():
    return psutil.disk_usage('/').percent


def current_ip():
    url = 'https://api.ipify.org?format=json'
    responce = requests.get(url)
    return responce.json()['ip']


def main():
    register_system()
    timeout = int(config.get('MAIN', 'timeout'))
    host = config.get('MAIN', 'host')
    while True:
        payload = {
            'serial': get_serial(),
            "cpu_load": get_cpu_load(),
            "memory_usage": memory_usage(),
            "disk_usage": disk_usage(),
            "ip_address": current_ip()
        }
        requests.post(host + '/info', data=json.dumps(payload))
        print('Request sent')
        sleep(timeout)


main()









