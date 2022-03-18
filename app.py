#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import requests
from prettytable import PrettyTable
from colorama import Fore, Back

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

headers1 = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'kw_token=A6GBL9WOLK',
    'csrf': 'A6GBL9WOLK',
    'Host': 'www.kuwo.cn',
    'Referer': 'http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%B7%B1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
}

headers2 = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'kw_token=OSFWJFXDRFA',
    'Host': 'www.kuwo.cn',
    'Referer': 'http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%B7%B1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
}

artist_name = input('请输入要搜索的歌手名字：')

response = requests.get(f'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={artist_name}&pn=1&rn=30&httpsStatus=1&reqId=9f235cc1-a61d-11ec-911e-49a496fc3a61', headers=headers1)
data_list = response.json()['data']['list']

tb = PrettyTable()
tb.field_names = ['歌曲ID', '艺术家', '歌曲名称', '所属专辑', '发布时间', 'mp3下载地址']

#声明2个列表变量,用来存放数据便于待会通过ID下载对应歌曲
all_rid = []  #放置歌曲ID
name_url = []  #放置歌曲名字和歌曲url地址

for i in data_list:
    musicrid = i['musicrid'].replace('MUSIC_', '')  #歌曲ID
    artist = i['artist']  #艺术家
    name = i['name']  #歌曲名称
    album = i['album']  #专辑
    releaseDate = i['releaseDate']  #发布时间

    music_response = requests.get(f'http://www.kuwo.cn/api/v1/www/music/playUrl?mid={musicrid}&type=music&httpsStatus=1&reqId=9f235cc1-a61d-11ec-911e-49a496fc3a61', headers=headers2)
    result = music_response.json()
    mp3_url = result['data']['url'] if result['code'] == 200 else '该歌曲为付费内容，请下载酷我音乐客户端后付费收听'

    all_rid.append(musicrid)
    name_url.append([name, mp3_url])

    tb.add_row([Fore.LIGHTRED_EX + musicrid + Fore.RESET, Back.RED + artist + Back.RESET, Fore.LIGHTGREEN_EX + name + Fore.RESET, album, releaseDate, mp3_url])

print(tb.get_string())

down_list = dict(zip(all_rid, name_url))

mp3_id = input('请输入要下载歌曲的ID：')
music = requests.get(down_list[mp3_id][1], headers=headers).content
with open(down_list[mp3_id][0] + '.mp3', 'wb') as f:
    f.write(music)