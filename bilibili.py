# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 11:23:40 2022

@author: illusory
"""
import os
import random
import re
import json
import requests

url = 'https://ip.jiangxianli.com/api/proxy_ip'
r = requests.get(url)
proxy = {'HTTP': 'http://' + r.json()['data']['ip'] + ':' + r.json()['data']['port']}

class BiLiBiLi():
    def __init__(self, s_url):
        self.url = s_url
        self.header = {
            'Range': 'bytes=0-',
            'referer': self.url,
            'origin': 'https://www.bilibili.com/',
            'Cookie': "your cookie",
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63'
        }

    def BL_download(self):
        html = requests.get(self.url, headers=self.header).text
        json_data = re.findall('window.__playinfo__=(.*?)</script>', html)[0]
        video_name=re.findall(',"title":"(.*?)","', html)[0]
        if video_name == '':
            video_name = int(random.random() * 2 * 1000)
        if len(str(video_name)) > 20:
            video_name = video_name[:20]
        video = json.loads(json_data)['data']['dash']['video'][0]['baseUrl']
        self.download(video,path,video_name,"flv")
        print("【BiLiBiLi】: {} 视频下载完成！".format(video_name))
        audio = json.loads(json_data)['data']['dash']['audio'][0]['baseUrl']
        self.download(audio, path,video_name,'mp3')
        print("【BiLiBiLi】: {} 音频下载完成！".format(video_name))


    def download(self,url,rel_path,video_name,ftype):
        r = requests.get(url, headers=self.header)
        rel_path += ftype +  "/"
        if os.path.exists(rel_path) == 0:
            os.mkdir(rel_path)
        rel_path += video_name + "." + ftype
        with open(rel_path, 'wb')as f:
            f.write(r.content)

def user_ui(bvid):
    share_url = "https://www.bilibili.com/video/"+bvid
    BiLiBiLi(share_url).BL_download()

if __name__ == '__main__':
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    }
    target_users = [{'user_name': 'up主姓名', 'target_user_id': 'up主id', 'pages_num': 10}]#一页一般30视频
    for user in target_users:
        user_id = user['target_user_id']
        user_name = user['user_name']
        pages_num = user['pages_num']
        path = 'D:/bilibili/'+user_name+"/"
        if os.path.exists(path) == 0:
            os.mkdir(path)        
        for page in range(1, pages_num + 1):
            count = 1
            print("正在爬取第" + str(page) + "页数据\n")
            user_main_page_link = "https://api.bilibili.com/x/space/arc/search?mid=" + user_id + "&ps=30&tid=0&pn=" + str(
                page) + "&keyword=&order=pubdate&jsonp=jsonp"
            user_response = requests.get(user_main_page_link, headers=headers)
            user_json = json.loads(user_response.text)
            user_datas = user_json['data']
            ls = user_datas['list']
            vlist = ls['vlist']
            for t in vlist:
                bvid = t['bvid']  # 视频id
                print("已经爬取第" + str(count) + "条\n")
                count += 1
                user_ui(bvid)



