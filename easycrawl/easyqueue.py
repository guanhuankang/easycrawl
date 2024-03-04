import time, random
from easybucket import easyBucket
from .tools import md5

class EasyQueue:
    def __init__(self, name, cache_size=1024):
        self.name = name
        self.cache_size = cache_size
         
        self.visited_router = lambda hash: f"{name}/visisted/{hash[0:3]}"
        self.dump_router = lambda hash: f"{name}/dump/{hash}"
        self.queue_router = lambda : f"{name}/queue"
    
    def push(self, hash, data):
        with easyBucket(self.queue_router()) as bucket:
            bucket["queue"] = self.tryDump(bucket.get("queue", []) + [(0, hash, data)])
            bucket["length"] = bucket.get("length", 0) + 1
            bucket["total"] = bucket.get("total", 0) + 1
            self.setVisitedData(hash, push=1)
    
    def pop(self, default=None):
        hash = default
        data = default
        with easyBucket(self.queue_router()) as bucket:
            queue = bucket["queue"]
            if len(queue) > 0:
                ret = queue.pop(0)
                while ret[0] > 0:
                    queue = self.tryDump(self.load(ret[1]) + queue)
                    ret = queue.pop(0)
                assert ret[0] == 0, f"Load Queue: {ret}"
                hash, data = ret[1], ret[2]
                bucket["queue"] = queue
                bucket["length"] = bucket["length"] - 1
                self.setVisitedData(hash, pop=1)
        return hash, data
    
    def size(self):
        size = 0
        with easyBucket(self.queue_router()) as bucket:
            size = bucket["length"]
        return size
    
    def has(self, hash):
        info = self.info(hash)
        return info["push"] > info["pop"]
    
    def visited(self, hash):
        info = self.info(hash)
        return info["push"] > 0
    
    def setVisitedData(self, hash, push=0, pop=0, data={}):
        with easyBucket(self.visited_router(hash)) as vbucket:
            vbucket[hash] = vbucket.get(hash, {"push": 0, "pop": 0, "data": {}})
            vbucket[hash]["push"] += push
            vbucket[hash]["pop"] += pop
            vbucket[hash]["data"].update(data)
            
    def info(self, hash):
        with easyBucket(self.visited_router(hash)) as vbucket:
            info = vbucket.get(hash, {"push": 0, "pop": 0, "data": {}})
        return info

    #### 
    def tryDump(self, queue):
        n = len(queue)
        if n >= self.cache_size:
            dump_queue = queue[n//2::]
            dump_hash = md5(str(time.time())+"-"+str(random.random()))
            with easyBucket(self.dump_router(dump_hash)) as dbucket:
                dbucket["queue"] = dump_queue
                dbucket["length"] = len(dump_queue)
            queue = queue[0:n//2] + [(1, dump_hash, None)]
        return queue
    
    def load(self, hash):
        with easyBucket(self.dump_router(hash)) as lbucket:
            queue = lbucket.get("queue", [])
            lbucket["length"] = 0
            lbucket["queue"] = []
        easyBucket.delete(self.dump_router(hash))
        return queue
    
if __name__=="__main__":
    eq = EasyQueue(name="testQueue")
    v = 0
    for i in range(10000):
        eq.push(md5(str(i)), i)
        print("push", i, end="\r")
        if random.random() < 0.2:
            hash, value = eq.pop()
            print("pop", value, end="\r")
            assert v==value
            v += 1
    _ = input(f"current size: {eq.size()} should be closed to 8000...")
    while eq.size() > 0:
        hash, value = eq.pop()
        print("pop", value, end="\r")
        assert v==value
        v += 1
    print("")
    print(eq.size(), v)
    easyBucket.clean()