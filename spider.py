import requests
import bs4
import datetime
def get_tnfsh_news_raw()->list:
    url='https://www.tnfsh.tn.edu.tw/latestevent/Index.aspx?Parser=9,3,19'
    web_page_text=requests.get(url).text
    web_page_dom=bs4.BeautifulSoup(web_page_text,'html.parser')
    result=web_page_dom.find_all('ul')[18].find_all('li')
    p=[]
    for item in result[1:]:
        link=item.find('a').get('href')
        title=item.find('a').get('title')
        date_str=item.find_all('span',class_='w15 hidden-xs')[1].text
        y,m,d=map(int,date_str.split('-'))
        date=datetime.date(year=y,month=m,day=d)
        link=link[link.find('=')+1:]
        p.append({'title':title,'date':date,'link':link})
    p.sort(key=lambda arg: arg['date'])
    return p

from collections import deque
import pickle
def get_tnfsh_new()->list:
    try:
        with open('news_deque.pkl','rb') as file:
            news_deque=pickle.load(file)
    except: news_deque=deque()
    
    raw_list=get_tnfsh_news_raw()
    now_date=datetime.date.today()
    while True:
        if len(news_deque)==0: break
        if (now_date-news_deque[0]['date']).days>5: news_deque.popleft()
        else: break
    idx=len(news_deque)
    for i in range(len(news_deque)-1,-1,-1):
        if news_deque[i]['link']==raw_list[0]['link']:
            idx=i
            break
    idx=len(news_deque)-idx
    news_deque.extend(raw_list[idx:])
    with open('news_deque.pkl','wb') as file:
        pickle.dump(news_deque,file)
    return raw_list[idx:]

def news_to_str(news:dict):
    link_prefix='https://www.tnfsh.tn.edu.tw/latestevent/Details.aspx?Parser='
    return f"{news['date']} {news['title']}\n{link_prefix}{news['link']}"

import time
def main():
    for _ in range(5):
        tmp=get_tnfsh_new()
        if len(tmp)==0: print('no news QQ')
        for item in tmp:
            print(item)
        time.sleep(5)

if __name__=='__main__': main()