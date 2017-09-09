try:
    import utime as time
except ImportError:
    import time
import _thread

lock = _thread.allocate_lock()

def thread_entry(e):
    lock.acquire()
    print('have it: ', e)
    time.sleep(1)
    lock.release()

# spawn the threads
for i in range(4):
    _thread.start_new_thread(thread_entry, (i,))

# wait for threads to finish
time.sleep(1)
print('done')