import json
import requests

url = 'http://paste.0x06.org/api/json/create'

payload = {'data':'foo','language':'text'}

headers = {'content-type': 'application/json'}

r = requests.post(url, data=json.dumps(payload), headers=headers)

res = json.loads(r.text)

print("http://paste.0x06.org/" + res['result']['id'])
