import ftpd
import _thread as th
import gc
gc.collect()
th.start_new_thread(ftpd.ftpserver, ('root', '12345'))
gc.collect()
