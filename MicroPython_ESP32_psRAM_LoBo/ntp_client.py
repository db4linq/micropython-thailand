import machine, network, utime
rtc = machine.RTC()
rtc.ntp_sync(server="pool.ntp.org")
utime.sleep(2)
rtc.synced()
while True:
  _tm = utime.localtime()
  print('{0}/{1}/{2} {3}:{4}:{5}'.format(_tm[2], _tm[1], _tm[0], _tm[3] + 6, _tm[4], _tm[5]))
  utime.sleep(1)