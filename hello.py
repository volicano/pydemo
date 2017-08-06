
# coding: utf-8

# In[ ]:

import requests
from bs4 import BeautifulSoup
res = requests.get('http://news.sina.com.cn/china/')
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text,'html.parser')


# In[2]:

import requests
from bs4 import BeautifulSoup
res = requests.get('http://news.sina.com.cn/china/')
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text,'html.parser')

import requests
from bs4 import BeautifulSoup
res = requests.get('http://news.sina.com.cn/china/')
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text,'html.parser')
# In[12]:

for news in soup.select('.news-item'):
    if len(news.select('h2')) > 0:
        h2 = news.select('h2')[0].text
        time = news.select('.time')[0].text
        a = news.select('a')[0]['href']
        print(time,h2,a)


# In[14]:

import requests
from bs4 import BeautifulSoup
res = requests.get('http://news.sina.com.cn/c/gat/2017-08-06/doc-ifyitapp1436210.shtml')
res.encoding = 'utf-8'
#print(res.text)
soup = BeautifulSoup(res.text,'html.parser')


# In[15]:

soup.select('#artibodyTitle')[0].text


# In[20]:

timeosource = soup.select('.time-source')[0].contents[0].strip()
type(timeosource)


# In[22]:

from datetime import datetime
dt = datetime.strptime(timeosource,'%Y年%m月%d日%H:%M')


# In[23]:

dt.strftime('%Y-%m-%d')


# In[25]:

soup.select('.time-source span a')[0].text


# In[35]:

article = []
for p in soup.select('#artibody p')[:-1]:
    article.append(p.text.strip())
print(article)
'  '.join(article)


# In[37]:

' '.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])


# In[39]:

soup.select('.article-editor')[0].text.lstrip('责任编辑：')


# In[41]:

import requests
comments = requests.get('http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-fyitamv5861883&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20&jsvar=loader_1501992399483_15389550')
import json
jd = json.loads(comments.text.strip('var loader_1501992399483_15389550='))


# In[42]:

jd['result']['count']['total']


# In[47]:

newsurl = 'http://news.sina.com.cn/c/nd/2017-08-06/doc-ifyitamv5861883.shtml'
newsid = newsurl.split('/')[-1].rstrip('.shtml').lstrip('doc-i')
print(newsid)


# In[51]:

import re
m = re.search('doc-i(.+)',newsurl)
newurl = m.group(1)
(newsid)


# In[52]:

commentURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-fyitamv5861883&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20&jsvar=loader_1501992399483_15389550'
commentURL.format(newsid)


# In[59]:

import re
import json

def getCommentCounts(newsurl):
    m = re.search('doc-i(.+).shtml',newsurl)
    newsid = m.group(1)
    comments = requests.get(commentURL.format(newsid))
    jd = json.loads(comments.text.strip('var loader_1501992399483_15389550='))
    return jd['result']['count']['total']


# In[60]:

news = 'http://news.sina.com.cn/c/nd/2017-08-06/doc-ifyitamv5861883.shtml'

getCommentCounts(news)


# In[62]:

import requests
from bs4 import BeautifulSoup

def getNewsDetail(newsurl):
    result = {}
    res = requests.get(newsurl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,'html.parser')
    result['title'] = soup.select('#artibodyTitle')[0].text
    result['newssource'] = soup.select('.time-source span a')[0].text
    timesource = soup.select('.time-source')[0].contents[0].strip()
    result['dt'] = datetime.strptime(timesource,'%Y年%m月%d日%H:%M')
    result['article'] = ' '.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])
    result['editor'] = soup.select('.article-editor')[0].text.strip('责任编辑：')
    result['comments'] = getCommentCounts(newsurl)
    return result


# In[63]:

getNewsDetail('http://news.sina.com.cn/c/nd/2017-08-06/doc-ifyitamv5861883.shtml')


# In[77]:

import requests
import json
res = requests.get('http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=4&callback=newsloadercallback&_=1502031793721')
jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
#jd


# In[82]:

for ent in jd['result']['data']:
    print(ent['url'])


# In[89]:

def parseListLinks(url):
    newsdetails = []
    res = requests.get(url)
    jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
    for ent in jd['result']['data']:
        newsdetails.append(getNewsDetail(ent['url']))
    return newsdetails


# In[90]:

url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=4&callback=newsloadercallback&_=1502031793721'
parseListLinks(url)


# In[95]:


url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1502033747337'
for i in range(1,10):
    print(url.format(i))


# In[116]:

url = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}&callback=newsloadercallback&_=1502033747337'
news_total = []
for i in range(1,2):
    newsurl = url.format(i)
    newsary = parseListLinks(newsurl)
    news_total.extend(newsary)


# In[108]:

len(news_total)


# In[117]:

import pandas
df = pandas.DataFrame(news_total)
df


# In[119]:

df.to_excel('news.xlsx')


# In[120]:

import sqlite3
with sqlite3.connect('news.sqlite') as db:
    df.to_sql('news',con=db)


# In[122]:

import sqlite3
with sqlite3.connect('news.sqlite') as db:
    df2 = pandas.read_sql_query('SELECT * FROM news',con=db)


# In[123]:

df2


# In[ ]:



