import re
import requests
from random import choice
from bs4 import BeautifulSoup
from selenium import webdriver

###############    All video source goes here     ###############

videos_source = {}
videos_source['popnews'] = []
videos_source['pearvideo'] = []
videos_source['chinanews'] = []
videos_source['popnews'].append('http://pop.stheadline.com/section.php?cat=new')   # Pop News 最新
videos_source['popnews'].append('http://pop.stheadline.com/section.php?cat=a')     # Pop News 港闻
videos_source['popnews'].append('http://pop.stheadline.com/section.php?cat=f')     # Pop News 娱乐
videos_source['popnews'].append('http://pop.stheadline.com/section.php?cat=b')     # Pop News 国际
videos_source['popnews'].append('http://pop.stheadline.com/section.php?cat=e')     # Pop News 两岸
videos_source['popnews'].append('http://pop.stheadline.com/section.php?cat=l')     # Pop News 生活
videos_source['popnews'].append('http://pop.stheadline.com/section.php?cat=m')     # Pop News 电影
videos_source['pearvideo'].append('https://www.pearvideo.com/category_2')          # 梨视频 世界
videos_source['chinanews'].append('https://www.chinanews.com/shipin/')             # 中新网

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


# 视频内容下载器
def video_downloader(file_name, download_link):
    supported_video_format = ['mp4']
    format_supported = False
    for video_format in supported_video_format:
        if video_format in download_link:
            format_supported = True
    if not format_supported:
        print('视频格式不支持: %s' % download_link)
        return

    req = requests.get(download_link)
    with open(file_name, 'wb') as f:
        f.write(req.content)
        f.close()
    print("{} downloaded".format(file_name))


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


# 捉取POPNEWS MP4链接
def pop_news_handler():
    for source in videos_source['popnews']:
        req = requests.get(source, headers=random_headers())
        soup = BeautifulSoup(html_decoder(req), 'html.parser')
        videos_list = soup.find('div', id='catPlayListB').find_all('div', class_='trailer')
        for video in videos_list:
            video_sub_page = 'http://pop.stheadline.com/' + video.find('a').get('href')
            video_title = video.find('a').get('title')
            req = requests.get(video_sub_page, headers=random_headers())
            driver = webdriver.Chrome(executable_path='C:\\Users\\Andy\\Downloads\\chromedriver.exe')
            driver.get(video_sub_page)
            if re.search('http.*\.mp4', driver.page_source):
                video_link = re.search('http.*\.mp4', driver.page_source).group(0)
                print(video_title, video_sub_page, video_link)
                driver.close()


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


# html 中文内容解码
def html_decoder(req):
    if not ('utf-8' in req.apparent_encoding.lower() or 'utf-8' in req.encoding.lower()):
        return req.content.decode('gbk')
    else:
        return req.text


def main():
    for source in videos_source:
        if source == 'popnews':
            pop_news_handler()
        elif source == 'pearvideo':
            pear_video_handler()
        elif source == 'chinanews':
            china_news_handler()

main()
