import machine, ubinasciiimport time, gcimport networkimport json, errnofrom machine import DHTfrom machine import Pin, I2C, Timer, ADCimport _thread as th 

timer1 = Timer(1)CLIENT_ID = ubinascii.hexlify(machine.unique_id())
power = ADC(Pin(33))adc = [ADC(Pin(32)), ADC(Pin(35)), ADC(Pin(34)), ADC(Pin(36)), ADC(Pin(39))]adc_config = [None, {'AirValue': 2200, 'WaterValue':1400}]d = DHT(Pin(16), DHT.DHT2X) _plant_no = None _mtt_config = None_read_interval = 20def load_config():  global _plant_no  global _mtt_config  global _read_interval  print('load configuration')  f = open('config.json')  cfg = json.loads(f.read())  f.close()  _plant_no = cfg['plant']  _mtt_config = cfg['mqtt']  _read_interval = cfg['read_interval']  return cfgdef read_soil(i):    global adc    sensor_count = 0  soilMoistureValue = 0    for _adc in adc:        sensorValue = _adc.read()        if sensorValue > 0:            sensor_count = sensor_count + 1            soilMoistureValue = soilMoistureValue + sensorValue              time.sleep(.2)    if sensor_count == 0:        return {'level': 0, 'raw': soilMoistureValue, 'msg': '(X)', 'sensor_count': sensor_count}    cfg = adc_config[i]      AirValue = cfg['AirValue']  WaterValue = cfg['WaterValue']      soilMoistureValue = int(soilMoistureValue / sensor_count)    if soilMoistureValue > AirValue:          cfg['AirValue'] = soilMoistureValue          AirValue = soilMoistureValue      if soilMoistureValue < WaterValue:          cfg['WaterValue'] = soilMoistureValue          WaterValue = soilMoistureValue   intervals = (AirValue - WaterValue)/3   result = None      if (soilMoistureValue >= WaterValue) and (soilMoistureValue <= (WaterValue + intervals)):            print("Very Wet")             result = {'level': 1, 'raw': soilMoistureValue, 'msg': '(^_^)', 'sensor_count': sensor_count};      elif (soilMoistureValue >= (WaterValue + intervals)) and (soilMoistureValue <= (AirValue - intervals)):            print("Wet")            result = {'level': 2, 'raw': soilMoistureValue, 'msg': '(*_*)', 'sensor_count': sensor_count};       elif (soilMoistureValue <= AirValue) and (soilMoistureValue >= (AirValue - intervals)):            print("Dry")            result = {'level': 3, 'raw': soilMoistureValue, 'msg': '(T_T)', 'sensor_count': sensor_count};       else:            result = {'level': 0, 'raw': soilMoistureValue, 'msg': '(X)', 'sensor_count': sensor_count};       return result
  
def read_data():
  global d 
  global CLIENT_ID
  global mqtt 
  topic = 'plant/{0}/temperature'.format(CLIENT_ID.decode("utf-8"))
  result , t, h = d.read() 
  if result:
    _tm = time.localtime()
    _strTime = '{0}/{1}/{2} {3}:{4}:{5}'.format(_tm[2], _tm[1], _tm[0], _tm[3] + 6, _tm[4], _tm[5])
    soil = {'id': 1, 'value': read_soil(1)}
    msg =  json.dumps({
        'Id': CLIENT_ID,                    
        'plant': _plant_no,
        'datetime': _strTime,
        'temperature': '{0:.2f}'.format(t), 
        'humidity': '{0:.2f}'.format(h),
        'soil': soil,
        'power': power.read()
    })
    print(topic, msg) 
    mqtt.publish(topic, msg)
  else:
    print('DHT Sensor read error') def loop_dht(o):  global d   global CLIENT_ID  global client   delay = o    while True:    try:      read_data()    except OSError as e:      if e.args[0] == errno.ETIMEDOUT:        print('error dht: ', e)            else:               import machine                machine.reset()    time.sleep(delay)
    
def subscb(task):
    print("[{}] Subscribed".format(task))
    def conncb(task):
  global _plant_no
  global mqtt  print("[{}] Connected".format(task)) 
  mqtt.subscribe('plant/{0}/temperature/get'.format(_plant_no))  _connected = True    def datacb(msg):
  global _plant_no
  global mqtt
    print("[{}] Data arrived from topic: {}, Message: ".format(msg[0], msg[1]), msg[2])
  if msg[1] == 'plant/{0}/temperature/get'.format(_plant_no):
    print(msg[1], msg)
    read_data()load_config()    mqtt = network.mqtt("myx", _mtt_config['broker'], secure=False, autoreconnect=20,
                          clientid=CLIENT_ID, keepalive = 30, retain=1, qos=0,  
                          connected_cb=conncb, data_cb=datacb, subscribed_cb=subscb)mqtt.start()
print('Wait mqtt connection...')time.sleep(1)th.start_new_thread('loop-dht',loop_dht, (_read_interval,))
print('Start main task...')