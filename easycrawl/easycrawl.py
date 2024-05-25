import time
from threading import Thread
from easybucket import easyBucket
from .easyqueue import EasyQueue
from .tools import md5

def __thread_set_and_check(idle, thread_id, n_threads):
    ret = True
    with easyBucket("easyCrawl/threads_manager") as bucket:
        bucket[str(thread_id)] = idle
        for tid in bucket.content():
            ret = ret and bucket[tid]
        bucket.flush()
    return ret

def thread_main(handler, queue, thread_id, n_threads):
    __thread_set_and_check(False, thread_id, n_threads)
    
    while True:
        hash, url = queue.pop()
        if hash==None:
            while not __thread_set_and_check(True, thread_id, n_threads) and queue.size()<=0:
                time.sleep(3)
            if __thread_set_and_check(True, thread_id, n_threads):
                print(thread_id, "I am sleeping (never die! hahah)", flush=True)
                time.sleep(1) ## return 
            __thread_set_and_check(False, thread_id, n_threads)
        else:
            handler(hash, url, queue)
        
class EasyCrawl:
    def __init__(self, entrances, handler, n_threads=8, easyqueue_name="easyqueue", easyqueue_cache_size=1024):
        self.queue = EasyQueue(name=easyqueue_name, cache_size=easyqueue_cache_size)
        for x in entrances:
            self.queue.push(x[0], x[1])
            
        self.threads = [
            Thread(target=thread_main, args=(handler, self.queue, thread_id, n_threads))
            for thread_id in range(n_threads)
        ]
        
    def start(self):
        for t in self.threads:
            t.start()
    
    def join(self):
        for t in self.threads:
            t.join()
        easyBucket.clean()
