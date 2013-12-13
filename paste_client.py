import json
import requests
import sys

# set the paste service api url
url = 'http://paste.0x06.org/api/json/create'

# read stuff from stdin
data = sys.stdin.read()

# build the payload
payload = {'data':data,'language':'text'}

# some headers
headers = {'content-type': 'application/json'}

# send the data to paste service
r = requests.post(url, data=json.dumps(payload), headers=headers)

# parse the json answer
res = json.loads(r.text)

# print the paste url
print("http://paste.0x06.org/" + res['result']['id'])
