import requests
import json
from authfire import *
import matplotlib.pyplot as plt

import time
import datetime
import pyrebase

start_time = time.time() # time for execute
now = datetime.datetime.now() # now time

firebase = pyrebase.initialize_app(CONFIG)
db = firebase.database()

from_date = '2018-07-15'
to_date = now.strftime('%Y-%m-%d')
bnk_name = 'bnk48official.orn'

req = requests.get(URL + from_date + '/' + to_date + '/posts/column_chart')
toJSON = json.loads(req.content)
orn = toJSON['collectors'][bnk_name]

arr_x = [] # date 
arr_y = [] # count

for i, item in enumerate(orn):
    db.child('orn').child(item['pcid']).child('url').set('http://facebook.com/'+item['pcid'])
    db.child('orn').child(item['pcid']).child('date').set(item['date'])
    db.child('orn').child(item['pcid']).child('comment_count').set(item['info']['comments_count'])
    db.child('orn').child(item['pcid']).child('share_count').set(item['info']['shares_count'])
    db.child('orn').child(item['pcid']).child('reactions').child('like').set(item['info']['reactions']['like'])
    db.child('orn').child(item['pcid']).child('reactions').child('wow').set(item['info']['reactions']['wow'])
    db.child('orn').child(item['pcid']).child('reactions').child('sad').set(item['info']['reactions']['sad'])
    db.child('orn').child(item['pcid']).child('reactions').child('love').set(item['info']['reactions']['love'])
    db.child('orn').child(item['pcid']).child('reactions').child('haha').set(item['info']['reactions']['haha'])
    db.child('orn').child(item['pcid']).child('reactions').child('angry').set(item['info']['reactions']['angry'])
    arr_x.append(item['date'].split('-')[1]+'-'+item['date'].split('-')[2])
    arr_y.append(item['info']['reactions']['like'])

plt.title('Likes count')
plt.plot(arr_x, arr_y)
plt.xlabel('date')
plt.ylabel('count')
plt.show()

print("--- %s seconds ---" % (time.time() - start_time))