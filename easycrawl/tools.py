import hashlib

def md5(data):
    if isinstance(data, str):
        data = bytes(data, encoding="utf8")
    md5_hash = hashlib.md5(data).hexdigest()
    return md5_hash

def getDomain(url):
    protocal = ""
    domain = ""
    path = url if url.startswith("/") else "/"+url
    for prefix in ["https://", "http://"]:
        if url.startswith(prefix):
            protocal = prefix
            domain = url[len(prefix)::].split("/")[0]
            path = url[len(prefix)+len(domain)::]
            path = path if path.startswith("/") else "/"+path
    return protocal, domain, path

def getHeaders(url, cookies=""):
    assert url.startswith("https://") or url.startswith("http://"), "URL Format ERROR:" + str(url)
    _, host, path = getDomain(url)
    return {
        "Host": host,
        "Method": "GET",
        "Path": path,
        "Scheme": "https",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": cookies,
        "Sec-Ch-Ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Microsoft Edge\";v=\"122\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    }
