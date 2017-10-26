import urequests
import json
TOKEN = 'IX1RkhYoWtVnfpRKkxVHJKedPosV7hO/XYHsWRQ09ai0DV0YuBHN9SNOFFXijiU2IYlTNFJB/qkdx49RuztNbdr3JyLb4Q7duN48ulGeUrWN8rzj3g5aDeWg+baY4akHER3FKDAaa7mtVZQ2xvnM4AdB04t89/1O/w1cDnyilFU=' 
URL = 'https://api.line.me/v2/bot/message/push'
headers = {'Content-Type':'application/json','Authorization': 'Bearer ' + TOKEN}

msg = json.dumps({'to': 'U48ac0b2b1efc36e219747f5181c11ba1', 'messages': [{'type': 'text', 'text': 'Hello World'}]})
r = urequests.post(URL , headers=headers, data=msg)
print(r.content)
r.close()