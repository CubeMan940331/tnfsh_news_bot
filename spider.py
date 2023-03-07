import httpx, datetime ,bs4, asyncio, pickle
from collections import deque

async def tnfsh_news_crawler()->list:
    '''
    grab information from the school website and return a list of news (sorted by timestamp)
    news is represented as {'title' : `str`, 'date' : `datetime.date`, 'link' : `str`}
    '''
    print(f'[{datetime.datetime.now()}] send request to source')
    url='https://www.tnfsh.tn.edu.tw/latestevent/Index.aspx?Parser=9,3,19'
    #url='https://www.tnfsh.tn.edu.tw/latestevent/Index.aspx?Parser=9,3,16'
    response=await httpx.AsyncClient().get(url)
    web_page_text=response.text
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

async def get_tnfsh_news()->list:
    '''
    return a list of news that haven't been forwarded
    '''
    try:
        with open('news_deque.pkl','rb') as file:
            news_deque=pickle.load(file)
    except: news_deque=deque()
    raw_list=await tnfsh_news_crawler()
    if len(news_deque)>100: news_deque=news_deque[-100:]
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

def news_to_str(news:dict)->str:
    '''
    convert news to str
    '''
    link_prefix='https://www.tnfsh.tn.edu.tw/latestevent/Details.aspx?Parser='
    return f"{news['date']} {news['title']}\n{link_prefix}{news['link']}"

#this section of code is for test
async def main():
    try:
        tmp=await get_tnfsh_news()
    except:
        print('cannot connect to source')
    else:
        if len(tmp)==0: print('no news detected')
        for item in tmp: print(item)

if __name__=='__main__': asyncio.run(main())
