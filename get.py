#!encoding=utf-8
import sys
sys.path.append('/home/bae/app/deps')
import requests
from bs4 import BeautifulSoup
import time
from tinydb import TinyDB, where

new = TinyDB('/home/bae/app/new.json')
old = TinyDB('/home/bae/app/old.json')
conte = TinyDB('/home/bae/app/conte.json')

new_urls = set()
for url in new.all():
    new_urls.add(url['url'])
#print(new_urls)
old_urls = set()
for url in old.all():
    old_urls.add(url['url'])
#print(old_urls)
def get_page(url):

    header = {"Accept":	"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          "Accept-Encoding"	:"gzip, deflate, br",
          "Accept-Language"	:"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
          "Connection":	"keep-alive",
          "Cookie":	'l_n_c=1; q_c1=81c4359eda6248bd9069a227b85784e0|1481644108000|1481644108000;\
           _xsrf=2aa44beda6e16bb9fe96d0cef4979349;\
            cap_id="YmQ4MmNmYjUxMGQ1NGRhYmFkZTJmMzdjNzk5N2VmZjk=|1481644108|6e14449598bd5e2519f85a8303e3b04dec449db8";\
             l_cap_id="ZjE0MmYyZTIzZTlmNDM0MmJlMWI4M2FhYWI4NjgxMTA=|1481644108|1554ec8de6957c9c49bc71669d5006220bd4bbe2";\
              n_c=1; d_c0="ADBCCGdL_gqPTntyYew254IAh8LLYBl3ELA=|1481644109"; \
              r_cap_id="YTVmY2IwMDkzNTQ2NDYzNmI2ZTljYWU4ODAwMjkwNmI=|1481644110|9b77e785189be7e9e13e79728c43cb05a1929223";\
               _zap=a284ab8d-9fc2-460d-bdec-c50e6c2f51b0;\
                __utma=51854390.611317762.1481644152.1481644152.1481644170.2;\
                 __utmb=51854390.4.10.1481644170; __utmc=51854390;\
                  __utmz=51854390.1481644170.2.2.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided);\
                   __utmv=51854390.000--|3=entry_date=20161213=1; __utmt=1',
          "Host": "www.zhihu.com",
          "Referer": url,
          "Upgrade-Insecure-Requests":	"1",
          "User-Agent":	"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
    }

    html = requests.get(url,headers=header).text.encode('GB18030').decode('GBK','ignore')
    pageSoup = BeautifulSoup(html,"html.parser")
    question = pageSoup.find(class_="zm-editable-content").get_text()
    items = pageSoup.find_all(class_="zm-item-answer")
    urls = pageSoup.find(id="zh-question-related-questions")
    return urls,items,question

def get_answer(item):
        try:
            vote = item.find('span', class_="js-voteCount").string
            #print(vote)
            name = item.find('a', class_="author-link").string
            summary = item.find(class_="zh-summary summary clearfix")
            summary.a.decompose()
            summary = summary.get_text()
            img = item.find(class_="zm-editable-content clearfix").find('img')
            content = item.find(class_="zm-editable-content clearfix").get_text()
            if int(vote)>100 and len(content)<200 and img is None:
                return name,vote,summary,content
            else:
                return
        except:
            return 

def get_urls(urls):
    try:
        for link in urls.find_all(class_="question_link"):
            url = link.get('href')
            if url is None:
                continue
            url = 'https://www.zhihu.com'+url
            if url not in new_urls and url not in old_urls and len(new_urls)<1000:
                new_urls.add(url)
                new.insert({'url':url})
    except:
        pass


if __name__ == '__main__':
    url = 'https://www.zhihu.com/question/30623666'
    if url not in new_urls and url not in old_urls:
        new_urls.add(url)
        new.insert({'url':url})
    i=0
   # print(len(new_urls))
    while len(new_urls) != 0 and i<2:
        new_url = new_urls.pop()
        new.remove(where('url')==new_url)
        old_urls.add(new_url)
        old.insert({'url':new_url})
        urls,items,question = get_page(new_url)
        get_urls(urls)
        i = i+1
        for item in items:
            try:
                #print('ceshiitem')
                name,vote,summary,content = get_answer(item)
                #print(question)
                if len(conte.all())>50:
                    conte.remove(where('question')==conte.all()[0]['question'])
                conte.insert({'question':question,'content':content})
                time.sleep(3)
            except:
                time.sleep(3)
                pass