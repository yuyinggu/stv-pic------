#! python
# -*- coding: utf-8 -*-
import re
import os
import pickle
import requests
import argparse
from ftplib import FTP
from time import sleep
from random import choice
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta


parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', required=True)
parser.add_argument('-p', '--password', required=True)
argv = parser.parse_args()


###############    All video source goes here     ###############
mp4_save_path = ''  # mp4文件保存路径
videos_source = {}
videos_source['popnews'] = []
videos_source['pearvideo'] = []
videos_source['chinanews'] = []
videos_source['itouchtv'] = []
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=new', '最新'])   # Pop News 最新
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=a', '港聞'])     # Pop News 港闻
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=f', '娛樂'])     # Pop News 娱乐
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=b', '國際'])     # Pop News 国际
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=e', '兩岸'])     # Pop News 两岸
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=l', '生活'])     # Pop News 生活
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=m', '電影'])     # Pop News 电影
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=c', '體育'])     # Pop News 体育
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=d', '財經'])     # Pop News 财经
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=s', '親子王'])     # Pop News 亲子王
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=ppl', '名人導航'])     # Pop News 名人导航
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=h', '地產'])     # Pop News 地產
videos_source['pearvideo'].append('https://www.pearvideo.com/category_2')          # 梨视频 世界
videos_source['chinanews'].append('https://www.chinanews.com/shipin/')             # 中新网
# videos_source['itouchtv'].append(['https://www.itouchtv.cn/', '推荐'])                        # 触电新闻 推荐
# videos_source['itouchtv'].append(['https://www.itouchtv.cn/news/funny', '搞笑'])              # 触电新闻 搞笑
#videos_source['itouchtv'].append(['https://www.itouchtv.cn/news/food', '美食'])              # 触电新闻 美食
# videos_source['itouchtv'].append(['https://www.itouchtv.cn/news/fashion', '时尚'])              # 触电新闻 时尚
videos_source['itouchtv'].append(['https://www.itouchtv.cn/news/video', '视频'])              # 触电新闻 视频

###############    All video sources go here     ###############

### 模拟浏览器 User-Agent
desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']


# 随机 浏览器 User-Agent
def random_headers():
    return {'User-Agent': choice(desktop_agents), 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


# 视频下载器
def video_downloader(file_path, file_name, download_link):
    supported_video_format = ['mp4']
    format_supported = False
    path = os.path.join(*[mp4_save_path, file_path, re.sub('\?|\|\*|\"', '', file_name) + '.mp4'])
    for video_format in supported_video_format:
        if video_format in download_link:
            format_supported = True
    if not format_supported:
        print('视频格式不支持: %s' % download_link)
        return
    if os.path.exists(path):
        print('{} 已存在'.format(path))
        return
    req = requests.get(download_link)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(path, 'wb') as f:
        f.write(req.content)
        f.close()
    print("{} downloaded {}".format(file_name, f.name))

# 捉取触电新闻MP4链接
def itouchtv_video_handler():
    for source in videos_source['itouchtv']:
        driver.maximize_window()
        # driver.set_page_load_timeout(30)
        try:
            driver.get(source[0])
        except:
            continue
        windows_height = driver.execute_script("return document.body.clientHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        while driver.execute_script("return document.body.clientHeight") > windows_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
            windows_height = driver.execute_script("return document.body.clientHeight")
            sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        videos_div = soup.findAll('div', {"class": "pushList__pushItem___bgsfJ"})
        for item in videos_div:
            video_sublink = item.find('a', {"class": "pushList__pushItemBox___2MME6"})['href']
            video_title = item.find('a', {"class": "pushList__pushItemBox___2MME6"})['title']
            print(video_sublink, video_title)
            driver.get('https://www.itouchtv.cn%s' % video_sublink)
            sleep(3)
            if re.search('src=\"(http.*?\.mp4)', driver.page_source):
                video_link = re.search('src=\"(http.*?\.mp4)', driver.page_source).group(1)
                print(video_title, video_link)
                video_downloader('itouchtv', video_title, video_link)


# 捉取梨视频MP4链接
def pear_video_handler():
    for source in videos_source['pearvideo']:
        req = requests.get(source, headers=random_headers())
        soup = BeautifulSoup(html_decoder(req), 'html.parser')
        videos_li = soup.find_all('li', class_='categoryem')
        for video in videos_li:
            video_title = video.find('div', class_='vervideo-title').string
            video_sub_page = 'https://pearvideo.com/' + video.find('a').get('href')
            req = requests.get(video_sub_page, headers=random_headers())
            if re.search('http.*\.mp4', html_decoder(req)):
                video_link = re.search('http.*\.mp4', html_decoder(req)).group(0)
                print(video_title, video_sub_page, video_link)
                video_downloader('pearvideo', video_title, video_link)



def pop_news_handler(selen_webdriver):
    """
    捉取POPNEWS MP4链接
    :param selen_webdriver: selenium webdrver
    :return: list [视频链接， 视频标题， 视频分类]
    """
    video_records = {}
    selen_webdriver.implicitly_wait(20)
    # driver.set_page_load_timeout(30)
    selen_webdriver.maximize_window()
    for source in videos_source['popnews']:
        req = requests.get(source[0], headers=random_headers())
        soup = BeautifulSoup(html_decoder(req), 'html.parser')
        # 类别页面出错handler 跳过
        try:
            videos_list = soup.find('div', id='catPlayListB').find_all('div', class_='trailer')
            for video in videos_list:
                video_sub_page = 'http://pop.stheadline.com/' + video.find('a').get('href')
                video_title = video.find('a').get('title')
                # req = requests.get(video_sub_page, headers=random_headers())
                try:
                    selen_webdriver.get(video_sub_page)
                except:
                    continue
                if re.search('http.*\.mp4', selen_webdriver.page_source):
                    video_link = re.search('http.*\.mp4', selen_webdriver.page_source).group(0)
                    print(video_title, video_sub_page, video_link)
                    video_records[os.path.basename(video_link)] = [video_title, source[1]]  # 视频链接， 视频标题， 视频分类
        except:
            pass
    selen_webdriver.close()
    return video_records


def popnews_ftp_comparor(selen_webdriver, debug_mode=False):
    """
    :param selen_webdriver: selenium webdrver
    :param debug_mode:
    :type debug_mode: boolean default False
        True: load video_records from pickle file
        False: run pop_news_handler() to get video_records
    """
    ftp_url = '203.80.0.177'
    user = argv.user
    passwd = argv.password
    today_date = (datetime.now() - timedelta(days=0)).strftime("%Y%m%d")  # 20180904

    if debug_mode:
        with open('test_records.pkl', 'rb') as f:
           video_records = pickle.load(f)
           f.close()
    else:
        video_records = pop_news_handler(selen_webdriver=selen_webdriver)
    # 保存 video_records 测试用途
    with open('test_records.pkl', 'wb') as f:
        pickle.dump(video_records, f)
        f.close()

    ftp = FTP(ftp_url)
    ftp.login(user, passwd)
    file_gen = ftp.mlsd('headline/%s' % today_date)
    ftp.dir('headline/%s' % today_date)
    csv_name = os.path.join(mp4_save_path, 'popnews%s.csv' % today_date)
    if os.path.exists(csv_name):
        os.remove(csv_name)

    videos_dict = {}
    for fg in file_gen:
        mp4_name = fg[0]
        if mp4_name in video_records:
            video_title = video_records[mp4_name][0]
            video_cat = video_records[mp4_name][1]
            if os.path.exists(csv_name):
                with open(csv_name, 'r', encoding='utf-8') as f:
                    f_content = f.read()
                    f.close()
                if mp4_name in f_content:
                    continue
        else:
            if os.path.exists(csv_name):
                with open(csv_name, 'r', encoding='utf-8') as f:
                    f_content = f.read()
                    f.close()
                if mp4_name in f_content:
                    continue
            video_title = ''
            video_cat = ''

        print("找到视频：{0} 标题：{1} 分类：{2}".format(mp4_name, video_title, video_cat))
        if not videos_dict.get(video_cat, None): videos_dict[video_cat] = {}
        videos_dict[video_cat][mp4_name] = {"video_title": video_title}
    with open(csv_name, 'w', encoding='utf-8') as f:
        write_str = ""
        for cat, val in videos_dict.items():
            for video_mp4_name, video_val in val.items():
                write_str += '{0},{1},{2}\n'.format(video_mp4_name,
                                                video_val['video_title'].replace(',', ' '),
                                                cat)
        f.write(write_str)
        f.close()


# 捉取中新网MP4链接
def china_news_handler():
    for source in videos_source['chinanews']:
        req = requests.get(source, headers=random_headers())
        soup = BeautifulSoup(html_decoder(req), 'html.parser')
        short_videos_div = (soup.find(href='http://www.chinanews.com/shipin/m/duan/views.shtml')
              .find_next(class_='splist')
              .find_all(class_='splist_div'))

        for div in short_videos_div:
            video_title = div.find('p').string
            video_sub_page = 'http://www.chinanews.com' + div.find('a').get('href')
            req = requests.get(video_sub_page, headers=random_headers())
            if re.search('http.*\.mp4', html_decoder(req)):
                video_link = re.search('http.*\.mp4', html_decoder(req)).group(0)
                print(video_title, video_sub_page, video_link)
                video_downloader('chinanews', video_title.strip(), video_link)


# html 中文内容解码
def html_decoder(req):
    if not ('utf-8' in req.apparent_encoding.lower() or 'utf-8' in req.encoding.lower()):
        return req.content.decode('gbk')
    else:
        return req.text


def main():
    for source in videos_source:
       if source == 'popnews':
           popnews_ftp_comparor(webdriver=driver)
#        if source == 'pearvideo':
#            pear_video_handler()
#        if source == 'chinanews':
#            china_news_handler()
#         if source == 'itouchtv':
#             itouchtv_video_handler()


# 下载对应版本Edge 驱动 https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# 放到此目录下
if os.path.exists('MicrosoftWebDriver.exe'):
    driver = webdriver.Edge(executable_path='MicrosoftWebDriver.exe')
elif os.path.exists('chromedriver.exe'):
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
else:
    print('缺少 web driver')
    exit(1)

try:
    main()
    driver.close()
    driver.quit()
except Exception as e:
    print(e)
    driver.close()
    driver.quit()
