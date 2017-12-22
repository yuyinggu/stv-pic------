import os
from PIL import ImageFont, Image, ImageDraw
import json
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import datetime,timedelta
import subprocess
from time import sleep
from opencc import OpenCC
# ---------------------------------------------------------
#全局设置
today = (datetime.now()).strftime("%Y-%m-%d") # 加 '+ timedelta(days=1)' 在now()后面测试明天的
today_list = today.split("-")
cons_path = "D:\\DayJobs\\STVPlayer\\星座、黃歷\\" #星座背景文件夹路径（不含文件名） 
cons_save = "\\\\vdisk.chineseradio.local\\VideoWork\\OtherVideos\\STPlayer\\Source\\"+ today_list[0]+"\\"+ today_list[1] +"\\"+ today_list[2] +"\\segment_02\\" #星座保存文件夹路径(不含文件名)
#video_path = "test.flv" #星座视频输出路径 + 文件名
huangli_path = "D:\\DayJobs\\STVPlayer\\星座、黃歷\\黃曆_Background.jpg" #黄历背景图片路径
huangli_save = "\\\\vdisk.chineseradio.local\\VideoWork\\OtherVideos\\STPlayer\\Source\\星座、黃歷\\test.jpg" #黄历输出图片路径+图片名
auto_close = 15 #成功后多少秒自动关闭
openCC = OpenCC('s2t')
font_dir = "C:\\Users\\helen.gu\\Documents\\GitHub\\stv-pic------\\"
# ---------------------------------------------------------
#获取星座数据
def getConstellation(cons):
    API_KEYS = "e162997788b7b704cbd48e9b9505da45"
    url = "http://web.juhe.cn:8080/constellation/getAll"
    params = {
        "key": API_KEYS,
        "consName": cons,
        "type": "today"
        }

    params = urlencode(params)
    # print(params)
    f = urlopen("%s?%s" % (url, params))
    res = json.loads(f.read().decode())
    # with open("星座.txt", "w") as f:
    #     f.write(json.dumps(res))
    return(openCC.convert(res["summary"]))

#---------------------------------------------------------
#修改十二星座的图片
def consImages():
    cons_list = ["摩羯座","水瓶座","双鱼座","白羊座","金牛座","双子座","巨蟹座","狮子座","处女座","天秤座","天蝎座","射手座"]
    for i,cons in enumerate(cons_list):
        print(i+1,cons)
        content = getConstellation(cons)
        temp = ""
        for j in range(len(content)):
            if j % 11 == 0 and j != 0:
                temp += ' \n' + content[j] + " "
            else: temp += content[j] + " "
        print(temp)

        #星座图片路径
        img_path = cons_path + cons + ".jpg"
        try:
            font = ImageFont.truetype(font_dir+"msyhbd.ttc",55,encoding='unic')
        except:
            input("\033[1;31;40m字体文件不存在\n")
            return
        try:
            im1 = Image.open(img_path)
        except OSError as e:
            input("\n\033[1;31;40m星座图片不存在或路径不对: " + e.strerror + "\033[0;40m")
            return
        draw = ImageDraw.Draw(im1)
        draw.text((550,300),temp ,(255,255,255),font=font)
        # draw.text((1200,300),result['summary'],(255,255,255),font=font)
        try:
            if i < 9:
                im1.save(cons_save + today_list[2] +"0"+ str(i+1) +".jpg")
            else:
                im1.save(cons_save + today_list[2] + str(i+1) +".jpg")
        except OSError as e:
            input(e.strerror)
            return False
        print("\n\033[1;32;40m%s图片生成成功\n\033[0;40m" % cons)

    return True
    # with open("星座.txt", "r") as f:
    #     result = f.readline()
    # result = json.loads(result)
    # print(result['summary'])
    #
    # # text = result['summary']


# ---------------------------------------------------------
#获取黄历数据 & 修改图片
def huangli():
    API_KEYS = "53dbd012b1d059f89396127e54539a70"
    reqUrl = "http://v.juhe.cn/laohuangli/d"
    params = {
        "key":API_KEYS,
        "date": today
    }
    params = urlencode(params)
    f = urlopen("%s?%s" % (reqUrl, params))
    res = json.loads(f.read().decode())
    # print(res["result"])
    #yangli = openCC.convert(res["result"]["yangli"].split("-"))
    yinli = openCC.convert(res["result"]["yinli"]) #阴历
    jishen = openCC.convert(res["result"]["jishen"]) #吉神
    xiongshen = openCC.convert(res["result"]["xiongshen"]) #凶神
    yi = openCC.convert(res["result"]["yi"]) #宜
    ji = openCC.convert(res["result"]["ji"]) #忌

    print("阴历: "+yinli + "\n吉神:\t"+jishen + "\n凶神:\t"+xiongshen + "\n宜:\t"+ yi + "\n吉:\t"+ji)

    # 黄历背景图片
    try:
        im1 = Image.open(huangli_path)
    except OSError as e:
        input("\033[1;31;40m黄历图片不存在或路径不对: \033[0;40m" + e.strerror)
        return
    else:
        print("\n黄历图片生成中...\n")

    draw = ImageDraw.Draw(im1)
    color = (0,99,49)
    width, height = im1.size
    #---------------------------------------------------------
    # 年月
    # "2017 年 12 月"
    # date = yangli[0]+ " 年 " + yangli[1] + " 月"
    # xPos = getMidPos(date, width, 36)
    # font = ImageFont.truetype("msyhbd.ttc",45,encoding='unic')
    # draw.text((xPos,40),date ,color,font=font)
    #---------------------------------------------------------
    # 日
    # day = yangli[2]
    # xPos = getMidPos(day, width, 170)
    # if int(day) < 10:
    #     xPos += 15
    # font = ImageFont.truetype("msyhbd.ttc",270,encoding='unic')
    # draw.text((xPos,30),day,color,font=font)
    #---------------------------------------------------------
    # 农历 yinli
    # "甲午(马)年八月十八"
    xPos = getMidPos(yinli, width, 30) #35pt 微软雅黑字体 约等于 30 pixel
    font = ImageFont.truetype(font_dir+"msyhbd.ttc",35,encoding='unic')
    draw.text((xPos,160),yinli ,color,font=font)
    #---------------------------------------------------------
    # 吉神 jishen
    # "官日 六仪 益後 月德合 除神 玉堂 鸣犬"
    temp = [""] * 2
    line = 0
    for i,val in enumerate(jishen.split(" ")):
        if i % 5 ==0 and i != 0:
            line += 1
            temp[line] = val + " "
        else:
            temp[line] += val + " "
    if line == 1:
        Y = [275,320]
    else:
        Y = [295]
    for i,Yposition in enumerate(Y): # 第一行 第二行  Y轴
        jishen = temp[i]
        xPos = getMidPos(jishen, width, 34) #20pt 微软雅黑字体 约等于 23 pixel
        font = ImageFont.truetype(font_dir+"msyhbd.ttc",30,encoding='unic')
        draw.text((xPos,Yposition),jishen ,color,font=font)
    #---------------------------------------------------------
    # 凶神 xiongshen
    # "月建 小时 土府 月刑 厌对 招摇 五离"
    temp = [""] * 2
    line = 0
    for i,val in enumerate(xiongshen.split(" ")):
        if i % 5 ==0 and i != 0:
            line += 1
            temp[line] = val + " "
        else:
            temp[line] += val + " "
    if line ==1:
        Y = [430,470]
    else:
        Y = [450]
    for i,Yposition in enumerate(Y): # 第一行 第二行  Y轴
        xiongshen = temp[i]
        xPos = getMidPos(xiongshen, width, 34) #20pt 微软雅黑字体 约等于 23 pixel
        font = ImageFont.truetype(font_dir+"msyhbd.ttc",30,encoding='unic')
        draw.text((xPos,Yposition),xiongshen ,color,font=font)
    #---------------------------------------------------------
    # 宜 yi
    # yi = "祭祀 出行 馀事勿取 扫舍"
    yiList = yi.split(" ")
    yi = ""
    line_words = 0 # Count How many words in one line if more than 6 characters new line
    font = ImageFont.truetype(font_dir+"msyhbd.ttc",30,encoding='unic')
    Ypos = 590
    for i,val in enumerate(yiList):
        if (line_words+len(val) > 6) and i < 14:
            xPos = getMidPos(yi, width/2, 34) #30pt 微软雅黑字体 约等于 34 pixel
            draw.text((xPos,Ypos),yi,color,font=font)
            Ypos += 35
            yi = yiList[i] + ' '
            line_words = len(val)
        elif i < 15:
            line_words += len(yiList[i])
            yi += yiList[i] + ' '

    xPos = getMidPos(yi, width/2, 34) # 30pt 微软雅黑字体 约等于 34 pixel
    draw.text((xPos,Ypos),yi,color,font=font)

    #---------------------------------------------------------
    # 忌 ji
    # ji = "祭祀 出行 馀事勿取 扫舍"
    jiList = ji.split(" ")
    ji = ""
    line_words = 0 # Count How many words in one line if more than 6 characters new line
    font = ImageFont.truetype(font_dir+"msyhbd.ttc",30,encoding='unic')
    Ypos = 590
    for i,val in enumerate(jiList):
        if (line_words+len(val) > 6) and i < 14:
            xPos = getMidPos(ji, width/2, 34) #30pt 微软雅黑字体 约等于 34 pixel
            draw.text((width/2+xPos+5,Ypos),ji,color,font=font)
            Ypos += 35
            ji = jiList[i] + ' '
            line_words = len(val)
        elif i < 15:
            line_words += len(jiList[i])
            ji += jiList[i] + ' '

    draw.text((width/2+xPos+5,Ypos),ji ,color,font=font)
    #---------------------------------------------------------
    #保存图片
    try:
        im1.save(huangli_save)
    except OSError as e:
        input("\n\033[1;31;40m 错误" + e.strerror + "\033[0;40m")
        return False
    else:
        print("\n\033[1;32;40m黄历图片生成成功\n\033[0;40m")
        return True

def getMidPos(string, width, pixel_word):
    wordsCount = 0
    for val in string.split(" "):
        wordsCount += len(val)
    xPos = (width/2)-((wordsCount*pixel_word)/2)
    return xPos


def test():
    # ----------------------------------------------------------测试星座图片修改
    # img_path = "C:\\Users\\Andy\\Pictures\\1.jpg"
    # font = ImageFont.truetype("msyhbd.ttc",55,encoding='unic')
    # im1 = Image.open(img_path)
    # draw = ImageDraw.Draw(im1)
    # draw.text((550,300),'搭理 我' ,(255,255,255),font=font)
    # im1.save("test.jpg")

    # ----------------------------------------------------------测试黄历
    print(datetime.now().strftime("%Y-%m-%d").split('-')[0])


def main():
    subprocess.call("",shell=True) #颜色
    cons_result = consImages() # 星座function
    h_result = huangli()       # 黄历function
    countDown = 0
    if cons_result and h_result:
        print("\033[1;32;40m \n星座，黄历图片生成完成\n\033[0;40m")
        while countDown < auto_close:
            print("\033[1;31;40m"+str(auto_close-countDown)+"\033[0;40m秒后自动关闭", end="\r")
            sleep(1)
            countDown += 1
    # test()

if __name__ == '__main__':
    main()
