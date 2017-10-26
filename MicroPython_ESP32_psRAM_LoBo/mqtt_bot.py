import timefrom umqtt import MQTTClientimport machine, ubinascii, gc, json import _thread as thfrom machine import Pin 
from machine import DHT
import urequests

class Btn1(Pin):  
  passclass Btn2(Pin):  
  pass  
  
TOKEN = 'IX1RkhYoWtVnfpRKkxVHJKedPosV7hO/XYHsWRQ09ai0DV0YuBHN9SNOFFXijiU2IYlTNFJB/qkdx49RuztNbdr3JyLb4Q7duN48ulGeUrWN8rzj3g5aDeWg+baY4akHER3FKDAaa7mtVZQ2xvnM4AdB04t89/1O/w1cDnyilFU=' URL = 'https://api.line.me/v2/bot/message/push'  btn1 = Btn1(18, Pin.IN)btn2 = Btn2(19, Pin.IN)led1 = Pin(21, Pin.OUT)led2 = Pin(22, Pin.OUT)
d = DHT(Pin(17), DHT.DHT2X)CLIENT_ID = ubinascii.hexlify(machine.unique_id())gc.collect()def sub_cb(topic, msg):  global oled  print((topic, msg))    if topic.decode('utf-8') == '/line/bot/gpio':    _obj =  json.loads(msg);    print(topic, _obj)    if _obj['pin'] == 21:      led1.value(_obj['status'])    if _obj['pin'] == 22:      led2.value(_obj['status'])  # get gpio status  if topic.decode('utf-8') == '/line/bot/goio/status/get':    _obj =  json.loads(msg);    if _obj['pin'] == 21:      client.publish('/line/bot/goio/status', json.dumps({'pin': 1, 'status': led1.value()}))    if _obj['pin'] == 22:      client.publish('/line/bot/goio/status', json.dumps({'pin': 2, 'status': led2.value()}))        if topic.decode('utf-8') == '/line/bot/goio/status/get/all':    p1 = {'pin': 1, 'status': led1.value() }    p2 = {'pin': 2, 'status': led2.value() }    client.publish('/line/bot/goio/status/all', json.dumps([p1, p2]))      
    if topic.decode('utf-8') == '/line/bot/temperature/get':    
      result , t, h = d.read()    
      print(result , t, h)    
    if result:      
      client.publish('/line/bot/temperature', json.dumps({'status': 1, 'temperature': '{0:.2f}'.format(t), 'humidity': '{0:.2f}'.format(h)}))    else:      
      client.publish('/line/bot/temperature', json.dumps({'status': 0, 'msg': 'invalid read temperature sensor'}))def _connect(): client.connect() client.subscribe('/line/bot/gpio') client.subscribe('/line/bot/goio/status/get') client.subscribe('/line/bot/goio/status/get/all')  client.subscribe('/line/bot/temperature/get')  client = MQTTClient(CLIENT_ID, 'iot.eclipse.org')
client.set_callback(sub_cb) 
_connect()
time.sleep(2)
print('Start main loop ...') 
def loop():    while True:    try:      client.wait_msg()    except OSError as e:      print (e)      time.sleep(3)      _connect()      

th.start_new_thread('send_push', send_push, ('Bot device start', ))  th.start_new_thread('loop', loop, ())
th.start_new_thread('btn1', btn_handler, (btn1,))
th.start_new_thread('btn2', btn_handler, (btn2,))