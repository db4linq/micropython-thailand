import untplibimport timeimport wifi_connect as wlanwlan.connect()c=untplib.NTPClient()resp=c.request('pool.ntp.org', version=3, port=123)print("Offset is ", resp.offset)i = 0while True:
  try:    tm = time.localtime(time.time() + resp.offset)    print('DATE TIME: {2:02d}/{1:02d}/{0} {3:02d}:{4:02d}:{5:02d}'.format(tm[0],tm[1],tm[2],tm[3]+7,tm[4],tm[5]))    time.sleep(1)
    i = i + 1
    if i == 300:
      print('sync ntp time server...')
      resp=c.request('pool.ntp.org', version=3, port=123)
      i = 0
  except untplib.NTPException as e:
    print (e)