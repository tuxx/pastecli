import json
import requests
import sys
import configparser

# read config file
config = configparser.ConfigParser()
config.read('pastecli.conf')
url = config['SERVICE']['url']
api = config['SERVICE']['api']
lang = config['OPTIONS']['lang']

# read stuff from stdin
data = sys.stdin.read()

# build the payload
payload = {'data':data,'language':lang}

# some headers
headers = {'content-type': 'application/json'}

# send the data to paste service
r = requests.post(api, data=json.dumps(payload), headers=headers)

# parse the json answer
res = json.loads(r.text)

# print the paste url
print(url + res['result']['id'])
