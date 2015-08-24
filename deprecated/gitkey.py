#import requests

#r = requests.get('https://github.com/laszewsk.keys')

#print r

#print r.text

#print r.json()


import urllib3
urllib3.disable_warnings()
http = urllib3.PoolManager()
r = http.request('GET','https://github.com/laszewsk.keys')
print r.status
print r.data


