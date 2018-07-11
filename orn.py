import requests
import json
from authfire import *

import time
import datetime
import pyrebase

from pymongo import MongoClient

start_time = time.time() # time for execute
now = datetime.datetime.now() # now time

connect = MongoClient('localhost', 27017)
db = connect.get_database('orn')
emp = db.fb_datas

from_date = '2018-07-01' # first day
to_date = now.strftime('%Y-%m-%d')
bnk_name = 'bnk48official.orn'

req = requests.get(URL + from_date + '/' + to_date + '/posts/column_chart')
toJSON = json.loads(req.content)
orn = toJSON['collectors'][bnk_name]

for i, item in enumerate(orn):
    fb_id, post_id = item['pcid'].split('_')
    emp.insert({
        "_id": post_id,
        "url": 'http://facebook.com/' + item['pcid'],
        "info": {
            "shares_count": item['info']['shares_count'],
            "reactions": {
                "wow": item['info']['reactions']['wow'],
                "sad": item['info']['reactions']['sad'],
                "love": item['info']['reactions']['love'],
                "like": item['info']['reactions']['like'],
                "haha": item['info']['reactions']['haha'],
                "angry": item['info']['reactions']['angry']
            },
            "comments_count": item['info']['comments_count']
        },
        "date": item['date']
    })

print("--- %s seconds ---" % (time.time() - start_time))