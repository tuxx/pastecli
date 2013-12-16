import json
import requests
import sys
import configparser
from os.path import expanduser

def get_config():
    user_conf = expanduser("~") + '/.pastecli.conf'
    global_conf = '/etc/pastecli.conf'
    list = []
    try:
        with open(user_conf):
            return user_conf
    except IOError:
        pass
    try:
        with open(global_conf):
            return global_conf
    except IOError:
        print('There must be a global or local config file')
        sys.exit()

if __name__ == "__main__":
    # read config file
    config = configparser.ConfigParser()
    config.read(get_config())
    url = config['SERVICE']['url']
    api = 'api/json/'
    lang = config['OPTIONS']['lang']
    expire = config['OPTIONS']['expire']

    # read stuff from stdin
    data = sys.stdin.read()

    # build the payload
    payload = {'data':data,'language':lang,'expire':expire}

    # some headers
    headers = {'content-type': 'application/json'}

    # send the data to paste service
    r = requests.post(url + api + 'create', data=json.dumps(payload), headers=headers)

    # parse the json answer
    res = json.loads(r.text)

    # print the paste url
    print(url + res['result']['id'])
