import requests
import json

res = requests.get('http://127.0.0.1:45533/api/account/check_fail?username=test')
print res.content
dic_res = json.loads(res.content)
print type(dic_res.get('result'))
if dic_res.get('result'):
    print 'should have verify pic code'
else:
    print 'no need'