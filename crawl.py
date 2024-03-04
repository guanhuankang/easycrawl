from easycrawl import EasyCrawl
from easycrawl import defaultHanlder, md5

if __name__=="__main__":
    urls = []
    entrances = [(md5(str(x)), x) for x in urls]
    
    easyCrawl = EasyCrawl(entrances=entrances, handler=defaultHanlder, n_threads=16)
    easyCrawl.start()
    easyCrawl.join()