
# coding: utf-8

# In[16]:

import requests
import json
import re
import os
import pymongo

from hashlib import md5
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from requests.exceptions import RequestException
from config import *
from multiprocessing import Pool

client = pymongo.MongoClient(MONGO_URL,connect=False)
db = client[MONGO_DB]

def get_page_index(offset,keyword):
    data = {
        'offset':offset,
        'format':'json',
        'keyword':keyword,
        'autoload':'true',
        'count':'20',
        'cur_tab':3
    }
    url='http://www.toutiao.com/search_content/?'+urlencode(data)
    try:
        respone = requests.get(url)
        if respone.status_code == 200:
            return respone.text
        return None
    except RequestException:
        print('请求索引出错')
        return None
def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')
def get_page_detail(url):
    try:
        reponse = requests.get(url)
        if reponse.status_code == 200:
            return reponse.text
        return None
    except RequestException:
        print('请求详情页出错',url)
        return None
    
def parse_page_detail(html,url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    print(title)
    image_pattern = re.compile('gallery: (.*?),\n',re.S)
    result = re.search(image_pattern,html)
    if result:
        data = json.loads(result.group(1))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:download_image(image)
            return {
                    'title':title,
                    'url':url,
                    'images':images
                    }

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('save success',result)
        return True
    return False

def download_image(url):
    print('正在下载:',url)
    try:
        reponse = requests.get(url)
        if reponse.status_code == 200:
            save_image(reponse.content)
        return None
    except RequestException:
        print('请求图片出错',url)
        return None

def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd()+"\images",md5(content).hexdigest(),'jpg')
    print(file_path)
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()
def main(offset):
    html = get_page_index(offset,KEYWORD)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            resutl = parse_page_detail(html,url)
            if resutl: save_to_mongo(resutl)
            
if __name__=='__main__':
    groups = [x*20 for x in range(GROUP_START,GROUP_END+1)]
    pool = Pool()
    pool.map(main,groups)
    


# In[ ]:



