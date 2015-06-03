#!/usr/bin/python
import json
import requests
import sys
import configparser
from os.path import expanduser
import argparse

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
    # argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--title',help='set the title of the paste',dest='title', default=None)
    parser.add_argument('-l','--lang',help='set the systax highlighting of the paste',dest='lang',default=config['OPTIONS']['lang'])
    parser.add_argument('--private',help='set if the paste should be private of the paste',action='store_true',dest='private', default=None)
    parser.add_argument('-p','--password',help='set the password for the paste',dest='password', default=None)
    parser.add_argument('-e','--expire',help='set the expire time of the paste in seconds',dest='expire', default=config['OPTIONS']['expire'])
    parser.add_argument('-u','--url',help='set the url of the paste service',dest='url', default=config['SERVICE']['url'] )
    args = parser.parse_args()

    api = 'api/json/'

    # check args
    r = requests.get(args.url+ api + 'parameter/language')
    res = json.loads(r.text)
    if args.lang not in res['result']['values']:
        print("the given language isn't valid please use one of these")
        print([x.encode('utf8') for x in res['result']['values']])
        exit()
    del r
    del res

    r = requests.get(args.url+ api + 'parameter/expire')
    res = json.loads(r.text)
    if int(args.expire) not in res['result']['values']:
        print("the given expire time isn't valide please use one of these")
        print(res['result']['values'])
        exit()
    del r
    del res

    # read stuff from stdin
    data = sys.stdin.read()

    # build the payload
    payload = {'data':data,'language':args.lang,'expire':args.expire}

    if args.title is not None:
        payload.update({'title':args.title})

    if args.private is not None:
        payload.update({'private':args.private})

    if args.password is not None:
        payload.update({'password':args.password})


    # some headers
    headers = {'content-type': 'application/json'}

    # send the data to paste service
    r = requests.post(args.url + api + 'create', data=json.dumps(payload), headers=headers)

    # parse the json answer
    res = json.loads(r.text)

    # print the paste url
    try:
		if res['result']['hash'] is not None:
			print(args.url + res['result']['id'] + '/' + res['result']['hash'])
		else:
			print(args.url + res['result']['id'])
    except KeyError:
        print res['result']['error']
