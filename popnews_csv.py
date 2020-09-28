# -*- coding: utf-8 -*-
import os
import pickle
import requests
import platform
import argparse
import logging
from time import sleep
import traceback

from ftplib import FTP
from random import choice
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta
import config_loader

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', required=False)
parser.add_argument('-p', '--password', required=False)
argv = parser.parse_args()

## 模拟浏览器 User-Agent
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


# videos_source( "popnews": [<URL>, <Category>, <Pages to load>])
videos_source = {}
videos_source['popnews'] = []
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=new', '最新', 2])   # Pop News 最新
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=a', '港聞', 2])     # Pop News 港闻
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=f', '娛樂', 1])     # Pop News 娱乐
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=b', '國際', 1])     # Pop News 国际
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=e', '兩岸', 1])     # Pop News 两岸
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=l', '生活', 1])     # Pop News 生活
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=m', '電影', 1])     # Pop News 电影
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=c', '體育', 1])     # Pop News 体育
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=d', '財經', 1])     # Pop News 财经
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=s', '親子王', 1])     # Pop News 亲子王
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=ppl', '名人導航', 1])     # Pop News 名人导航
videos_source['popnews'].append(['http://pop.stheadline.com/section.php?cat=h', '地產', 1])     # Pop News 地產



# html 中文内容解码
def html_decoder(req):
    if not ('utf-8' in req.apparent_encoding.lower() or 'utf-8' in req.encoding.lower()):
        return req.content.decode('gbk')
    else:
        return req.text


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

        print_log("找到视频：{0} 标题：{1} 分类：{2}".format(mp4_name, video_title, video_cat))
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
        # 类别页面出错handler 跳过
        try:
            print_log("打开 Popnews '{}' 分类网页".format(source[1]))
            selen_webdriver.get(source[0])
            soup = BeautifulSoup(selen_webdriver.page_source, 'html.parser')
            # 加载 popnews 第一页的MP4 url
            videos_list = soup.find_all('li', class_='trailer')
            for video in videos_list:
                video_info = video.find('a')
                video_link = video_info.attrs['data-video']
                video_title = video_info.attrs['title']
                print_log((video_title, video_link))
                video_records[os.path.basename(video_link)] = [video_title, source[1]]  # 视频链接， 视频标题， 视频分类
            # 加载 其他页的MP4 url
            try:
                if source[2] > 1:
                    for page_num in range(2, source[2]+1):
                        selen_webdriver.find_element_by_id("nextPage").click()
                        sleep(1)
                        news_videos_list = selen_webdriver.find_elements_by_class_name("module-wrap")
                        for video_session in news_videos_list:
                            video_title = video_session.text
                            video_link = video_session.find_element_by_css_selector("a").get_attribute('data-video')
                            print_log((video_title, video_link))
                            video_records[os.path.basename(video_link)] = [video_title, source[1]]
            except Exception as e:
                print_log(traceback.format_exc(), log_level='error')
        except Exception as err:
            print_log(err)
            continue
    selen_webdriver.close()
    return video_records


def random_headers():
    """
    随机 浏览器 User-Agent
    """
    return {'User-Agent': choice(desktop_agents), 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


def print_log(log_content, log_level='info'):
    print(log_content)
    if log_level == 'error':
        LOGGER.error(log_content)
    elif log_level == 'debug':
        LOGGER.debug(log_content)
    elif log_level == 'warn':
        LOGGER.warn(log_content)
    else:
        LOGGER.info(log_content)


def main():
    # 下载对应版本Edge 驱动 https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
    # 下载对应版本Chrome 驱动 https://chromedriver.chromium.org/
    # 放到此目录下
    headless = configs.conf_finder(section, 'headless', val_type=bool)
    if platform.system() == 'Windows':
        if driver_path.endswith("MicrosoftWebDriver.exe") and os.path.exists(driver_path):
            print_log("加载Edge驱动")
            driver = webdriver.Edge(executable_path=driver_path)
            print_log("驱动版本： {0}".format(driver.capabilities['version']))
        elif os.path.exists(driver_path):
            print_log("加载Chrome驱动")
            # options = webdriver.ChromeOptions()
            # options.add_argument('--headless')
            # options.add_argument('--start-maximized')
            # options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
            driver = webdriver.Chrome(executable_path=driver_path)
            print_log("驱动版本： {0}".format(driver.capabilities.get('chrome', dict()).get('chromedriverVersion', "UNKNOWN")))
        else:
            print_log('缺少 web driver', log_level='error')
            exit(1)
    elif platform.system() == 'Linux':
        if os.path.exists(driver_path):
            print_log("\u52a0\u8f7dChrome\u9a71\u52a8")
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument('headless')
            options.add_argument('window-size=1280x800')
            options.binary_location = '/opt/google/chrome/google-chrome'
            driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
            print_log("驱动版本： {0}".format(driver.capabilities.get('chrome', dict()).get('chromedriverVersion', "UNKNOWN")))
        else:
            print_log('缺少 web driver', log_level='error')
            exit(1)
    elif platform.system() == 'Darwin':
        if os.path.exists(driver_path):
            print_log("\u52a0\u8f7dChrome\u9a71\u52a8")
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument('headless')
            options.add_argument('window-size=1280x800')
            driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
            print_log("驱动版本： {0}".format(driver.capabilities.get('chrome', dict()).get('chromedriverVersion', "UNKNOWN")))
        else:
            print_log('缺少 web driver', log_level='error')
            exit(1)
    else:
        print_log("OS Platform {} does not support".format(platform.system()))
        exit(1)
    popnews_ftp_comparor(selen_webdriver=driver, debug_mode=False)
    driver.quit()
    print_log("Program Exit")


if __name__ == '__main__':
    LOGGER = logging.getLogger('popnews_csv')
    LOGGER.setLevel(logging.INFO)
    LOGFILE = 'popnews_csv.log'
    fileHandler = logging.FileHandler(LOGFILE, 'w', 'utf-8')
    LOGFORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
    fileHandler.setFormatter(LOGFORMAT)
    LOGGER.addHandler(fileHandler)
    configs = config_loader.ConfLoader()
    section = "default"
    mp4_save_path = configs.conf_finder(section, "mp4_save_path", r"")
    driver_path = configs.conf_finder(section, "web_driver_path")
    if not argv.user:
        argv.user = configs.conf_finder(section, "ftp_user")
    if not argv.password:
        argv.password = configs.conf_finder(section, "ftp_pass")
    main()
