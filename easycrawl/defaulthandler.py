import requests
import re
from bs4 import BeautifulSoup
import logging
import traceback
from easybucket import easyBucket
from .tools import md5, getDomain, getHeaders

def defaultHanlder(hash, url, queue):
    tot = None
    try:
        res = requests.get(url, headers=getHeaders(url))
        if res.status_code==200:
            page = BeautifulSoup(res.content, 'html.parser')
            alist = page.find_all('a')
            magnets = []
            outlinks = set()
            for a in alist:
                if a.get("href", "#").startswith("magnet:?xt"):
                    magnets.append({
                        "name": a.string.strip(),
                        "address": a["href"],
                        "url": url
                    })
                if re.search(r"/html.+\.html", a.get("href", "#")):
                    protocal, host, path = getDomain(a["href"])
                    if protocal == "":
                        protocal, host, _ = getDomain(url)
                        outlnk = protocal + host + path
                    else:
                        outlnk = protocal + host + path
                    outlinks.add(outlnk)
            
            if len(magnets) > 0:
                name = magnets[0]["name"]
                with easyBucket(f"movies/{name}") as bucket:
                    bucket["movies"] = magnets
                    bucket.flush()
                with easyBucket(f"movie_meta") as bucket:
                    bucket["num_movies"] = bucket.get("num_movies", 0) + 1
                    tot = bucket["num_movies"]
                    bucket.flush()
            
            for outlnk in outlinks:
                hash = md5(outlnk)
                if not queue.visited(hash):
                    queue.push(hash, outlnk)
                    
            queue.setVisitedData(hash, data={"status": 200, "url": url})
            
        elif res.status_code==429:
            queue.push(hash, url)
            queue.setVisitedData(hash, data={"status": 429, "url": url})
        else:
            queue.setVisitedData(hash, data={"status": res.status_code, "url": url})
    except Exception as e:
        logging.error(str(traceback.format_exc()))
    
    if tot==None:
        with easyBucket(f"movie_meta") as bucket:
            tot = bucket.get("num_movies", 0)
    print(f"Queue: {queue.size()}, Movies: {tot}    ", end="\r")