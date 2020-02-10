import requests
import re
import time
from lxml import etree
from tqdm.auto import tqdm
def getKey():
    resp = requests.get("http://www.google.com")
    html = resp.text
    key = re.search(r"kEI:\'(.*?)\'", html).group(1)
    return key
def search(query,key,verbose=False):
    url = f"https://www.google.com/search?source=hp&ei={key}&q={query}"
    print(">>> request on url: \n"+url)
    proxies = {"http":getAvailableProxy(),
               "https":getAvailableProxy()}
    print(">>> use proxy as follow: \n",proxies)
    print(">>> 本机ip:\n",json.loads(requests.get("http://httpbin.org/ip").text.strip()))
    print(">>> 代理ip:\n",json.loads(requests.get("http://httpbin.org/ip",proxies=proxies).text.strip()))
    header = {"Referer": "https://www.google.com/",
              'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
#     resp1 = requests.get(url,headers=header,proxies=proxies)
    resp1 = requests.get(url,headers=header)
    print(">>> result len:",len(resp1.text))
    if(verbose):
        with open("googleSearchResult_request.html","w+") as f: f.write(resp1.text)
    return resp1.text
def find_g(element):
    div_g = element.xpath("./div[@class='g']")
    if(len(div_g)==0):
        div_srg = element.xpath("./div[@class='srg']")
        if(len(div_srg)>0):
            div_g = div_srg[0].xpath("./div[@class='g']")
    return div_g
def find_result(element):
    a_el = element.xpath(".//div[@class='r']")[0].xpath("a")[0]
    title = a_el.xpath(".//h3[@class='LC20lb']")[0].text
    link = a_el.attrib["href"]
    summary = element.xpath(".//div[@class='s']")[0].xpath("string(.)")
    return [title,link,summary]
def parse(html_inp):
    html = etree.HTML(html_inp)
    # 查找所有class为g的div
    div_rso = html.xpath("//div[@id='rso']")
    div_bkWMgd = div_rso[0].xpath("./div[@class='bkWMgd']")
    div_g = []
    for el in div_bkWMgd:
        tmp = find_g(el)
        if(len(tmp)>0):
            div_g.extend(tmp)
    print(f"目标div (class为g) 有 {len(div_g)} 个")
    # 解析class为g的div
    result = [find_result(i) for i in div_g]
    return result
def getResult(query,key=getKey(),verbose=False):
    html_res = search(query,key,verbose)
    return parse(html_res)

with open("searchResult.txt","w+") as f:
    for query in tqdm(["BJP"]):
        print(f"current query at {query}")
        result = getResult(query,getKey(),True)
        result
