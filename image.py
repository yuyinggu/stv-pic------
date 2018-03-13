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
tomorrow = (datetime.now()+ timedelta(days=1)).strftime("%Y-%m-%d")
today_list = today.split("-")
tomorrow_list = tomorrow.split("-")
tomorrow_after = (datetime.now()+ timedelta(days=2)).strftime("%Y-%m-%d")
tomorrow_after_list = tomorrow_after.split("-")
cons_path = "\\\\vdisk.chineseradio.local\\it\\Jobs\\Constellation\\Photo\\"#"C:\\Users\\helen.gu\\Documents\\GitHub\\stv-pic------\\" #星座背景文件夹路径（不含文件名）
cons_save = "\\\\vdisk.chineseradio.local\\VideoWork\\OtherVideos\\STPlayer\\Source\\"+ tomorrow_list[0]+"\\"+ tomorrow_list[1] +"\\"+ tomorrow_list[2] +"\\"+"Constellation/" #星座保存文件夹路径(不含文件名)
#video_path = "test.flv" #星座视频输出路径 + 文件名
huangli_path = "\\\\vdisk.chineseradio.local\\it\\Jobs\\Constellation\\Photo\\Background-01.jpg" #黄历背景图片路径
huangli_path2 = "\\\\vdisk.chineseradio.local\\it\\Jobs\\Constellation\\Photo\\Background-02.jpg" #黄历背景图片路径
huangli_save = "\\\\vdisk.chineseradio.local\\VideoWork\\OtherVideos\\STPlayer\\Source\\"+ tomorrow_list[0]+"\\"+ tomorrow_list[1] +"\\"+ tomorrow_list[2] +"\\"+"SideAd/" #黄历输出图片路径+图片名
auto_close = 15 #成功后多少秒自动关闭
openCC = OpenCC('s2t')
font_dir = "\\\\vdisk.chineseradio.local\\it\\Jobs\\Constellation\\Photo\\"#"C:\\Users\\helen.gu\\Documents\\GitHub\\stv-pic------\\"
record_dir = "\\\\vdisk.chineseradio.local\\VideoWork\\OtherVideos\\STPlayer\\Source\\"+ tomorrow_list[0]+"\\"+ tomorrow_list[1] +"\\"+ tomorrow_list[2] +"\\"+ tomorrow_list[1] + tomorrow_list[2] + ".txt" #txt文件路径
txt_exist = False
if os.path.exists(record_dir):
    with open(record_dir, "r", encoding="utf8") as txt_file:
        if len(txt_file.readlines()) >= 36:
            txt_exist = True
        else:
            print("txt文件内容不符，跳过。。。。")
 # ---------------------------------------------------------
#获取星座数据
#聚合
def getConstellation(cons):
    global txt_file
    API_KEYS = "e162997788b7b704cbd48e9b9505da45"
    url = "http://web.juhe.cn:8080/constellation/getAll"
    params = {
        "key": API_KEYS,
        "consName": cons,
        "type": "today"
        }

    params = urlencode(params)
    # print(params)
    try:
        f = urlopen("%s?%s" % (url, params))
        res = json.loads(f.read().decode())

        if not txt_exist:
            with open(record_dir,"a",encoding='utf8') as txt_file:
                txt_file.write(cons+"\n")
                txt_file.write(openCC.convert(res["summary"])+"\n")
                txt_file.close()
    except:
        pass
    # with open("星座.txt", "w") as f:
    #     f.write(json.dumps(res))

    try:
        return(openCC.convert(res["summary"]))
    except:
        print("Error:无法拿到星座")
        return()

#showapi
def getConstellation2(cons):
    appid = "53341"
    secret = "d0e921caef0645f4bff676dba1a05a34"
    url = "http://route.showapi.com/872-1"
    params = {
        "showapi_appid": appid,
        "showapi_sign": secret,
        "star": cons,
        "needTomorrow": 0,
        "needWeek": 0,
        "needMonth": 0,
        "needYear": 0
        }

    params = urlencode(params)
    # print(params)
    f = urlopen("%s?%s" % (url, params))
    res = json.loads(f.read().decode())
    # with open("星座.txt", "w") as f:
    #     f.write(json.dumps(res))
    try:
        return(openCC.convert(res["showapi_res_body"]["day"]["day_notice"]))
    except:
        return()
#---------------------------------------------------------
#修改十二星座的图片
def checkconsPath(input_path):
    if input_path == "":
        return
    else:
        if not os.path.exists(input_path):
            print("文件夹不存在,创建文件夹：\n")
            os.makedirs(input_path)

def consImages():
    cons_list = ["摩羯座","水瓶座","双鱼座","白羊座","金牛座","双子座","巨蟹座","狮子座","处女座","天秤座","天蝎座","射手座"]
    cons_list2 = ["mojie","shuiping","shuangyu","baiyang","jinniu","shuangzi","juxie","shizi","chunv","tiancheng","tianxie","sheshou"]
    for i,cons in enumerate(cons_list):
        print(i+1,cons)

        if not txt_exist:
            content = getConstellation(cons)
        else:
            with open(record_dir, "r", encoding="utf8") as txt_file:
                result = txt_file.readlines()
                index = result.index(cons+"\n")
                content = result[index+1][:-1]

        temp = ""
        for j in range(len(content)):
            if j % 13 == 0 and j != 0:
                temp += ' \n' + content[j]
            else: temp += content[j]
        print(temp)

        #星座图片路径
        # img_path = cons_path + cons + ".jpg"
        img_path = cons_path + cons_list[i] + ".jpg"
        try:
            font = ImageFont.truetype(font_dir+"msyhbd.ttc",65,encoding='unic')
        except:
            input("\033[1;31;40m字体文件不存在\n")
            return
        try:
            im1 = Image.open(img_path)
        except OSError as e:
            input("\n\033[1;31;40m星座图片不存在或路径不对: " + e.strerror + "\033[0;40m")
            return
        draw = ImageDraw.Draw(im1)
        draw.text((435,230),temp ,(255,255,255),font=font)
        # draw.text((1200,300),result['summary'],(255,255,255),font=font)
        try:
            if i < 9:
                im1.save(cons_save + tomorrow_list[0] + tomorrow_list[1]+tomorrow_list[2] + "-" + "0"+ str(i+1) +".jpg",quality=100)
            else:
                im1.save(cons_save + tomorrow_list[0] + tomorrow_list[1]+tomorrow_list[2] + "-" + str(i+1) +".jpg",quality=100)
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
def get_huangli(day):
    API_KEYS = "53dbd012b1d059f89396127e54539a70"
    reqUrl = "http://v.juhe.cn/laohuangli/d"
    params = {
        "key":API_KEYS,
        "date": day
    }
    params = urlencode(params)
    f = urlopen("%s?%s" % (reqUrl, params))
    res = json.loads(f.read().decode())
    return(res)

def huangli(day,in_path,out_path,file_name):
    #如果txt文件不存在去API拿数据
    if not txt_exist:
        res = get_huangli(day)
        # print(res["result"])
        #yangli = openCC.convert(res["result"]["yangli"].split("-"))
        yinli = openCC.convert(res["result"]["yinli"]) #阴历
        jishen = openCC.convert(res["result"]["jishen"]) #吉神
        xiongshen = openCC.convert(res["result"]["xiongshen"]) #凶神
        yi = openCC.convert(res["result"]["yi"]) #宜
        ji = openCC.convert(res["result"]["ji"]) #忌

        with open(record_dir,"a",encoding='utf8') as txt_file:
            txt_file.write(day+"\n")
            txt_file.write(yinli+"\n")
            txt_file.write("宜"+"\n")
            txt_file.write(yi+"\n")
            txt_file.write("忌"+"\n")
            txt_file.write(ji+"\n")
            txt_file.close()

        print("阴历: "+yinli + "\n吉神:\t"+jishen + "\n凶神:\t"+xiongshen + "\n宜:\t"+ yi + "\n吉:\t"+ji)
    else:
        with open(record_dir, "r", encoding='utf8') as txt_file:
            result = txt_file.readlines()
            index = result.index(day+"\n")
            yinli = result[index+1][:-1]
            yi = result[index+3][:-1]
            ji = result[index+5][:-1]
            print("阴历: "+yinli + "\n宜:\t"+ yi + "\n吉:\t"+ji)
    # 黄历背景图片
    try:
        im1 = Image.open(in_path)
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
    # font = ImageFont.truetype("msyhbd.ttc",45,encoding='utf8')
    # draw.text((xPos,40),date ,color,font=font)
    #---------------------------------------------------------
    # 日
    # day = yangli[2]
    # xPos = getMidPos(day, width, 170)
    # if int(day) < 10:
    #     xPos += 15
    # font = ImageFont.truetype("msyhbd.ttc",270,encoding='utf8')
    # draw.text((xPos,30),day,color,font=font)
    #---------------------------------------------------------
    # 农历 yinli
    # "甲午(马)年八月十八"
    xPos = getMidPos(yinli, width, 35) #35pt 微软雅黑字体 约等于 40 pixel
    font = ImageFont.truetype(font_dir+"msyhbd.ttc",40,encoding='unic')
    draw.text((xPos,210),yinli ,color,font=font)
    #---------------------------------------------------------
    # 吉神 jishen
    # "官日 六仪 益後 月德合 除神 玉堂 鸣犬"
    # temp = [""] * 2
    # line = 0
    # for i,val in enumerate(jishen.split(" ")):
    #     if i % 5 ==0 and i != 0:
    #         line += 1
    #         temp[line] = val + " "
    #     else:
    #         temp[line] += val + " "
    # if line == 1:
    #     Y = [275,320]
    # else:
    #     Y = [295]
    # for i,Yposition in enumerate(Y): # 第一行 第二行  Y轴
    #     jishen = temp[i]
    #     xPos = getMidPos(jishen, width, 34) #20pt 微软雅黑字体 约等于 23 pixel
    #     font = ImageFont.truetype(font_dir+"msyhbd.ttc",30,encoding='utf8')
    #     draw.text((xPos,Yposition),jishen ,color,font=font)
    #---------------------------------------------------------
    # 凶神 xiongshen
    # "月建 小时 土府 月刑 厌对 招摇 五离"
    # temp = [""] * 2
    # line = 0
    # for i,val in enumerate(xiongshen.split(" ")):
    #     if i % 5 ==0 and i != 0:
    #         line += 1
    #         temp[line] = val + " "
    #     else:
    #         temp[line] += val + " "
    # if line ==1:
    #     Y = [430,470]
    # else:
    #     Y = [450]
    # for i,Yposition in enumerate(Y): # 第一行 第二行  Y轴
    #     xiongshen = temp[i]
    #     xPos = getMidPos(xiongshen, width, 34) #20pt 微软雅黑字体 约等于 23 pixel
    #     font = ImageFont.truetype(font_dir+"msyhbd.ttc",30,encoding='utf8')
    #     draw.text((xPos,Yposition),xiongshen ,color,font=font)
    #---------------------------------------------------------
    # 宜 yi
    # yi = "祭祀 出行 馀事勿取 扫舍"
    yiList = yi.split(" ")
    yi = ""
    line_words = 0 # Count How many words in one line if more than 6 characters new line
    font = ImageFont.truetype(font_dir+"msyhbd.ttc",40,encoding='unic')
    Ypos = 350
    for i,val in enumerate(yiList):
        if (line_words+len(val) > 10) and i < 11:
            xPos = getMidPos(yi, width, 45) #30pt 微软雅黑字体 约等于 34 pixel
            draw.text((xPos,Ypos),yi,color,font=font)
            Ypos += 45
            yi = yiList[i] + ' '
            line_words = len(val)
        elif i < 14:
            line_words += len(yiList[i])
            yi += yiList[i] + ' '

    xPos = getMidPos(yi, width, 45) # 30pt 微软雅黑字体 约等于 34 pixel
    draw.text((xPos,Ypos),yi,color,font=font)

    #---------------------------------------------------------
    # 忌 ji
    # ji = "祭祀 出行 馀事勿取 扫舍"
    jiList = ji.split(" ")
    ji = ""
    line_words = 0 # Count How many words in one line if more than 6 characters new line
    font = ImageFont.truetype(font_dir+"msyhbd.ttc",40,encoding='unic')
    Ypos = 600
    for i,val in enumerate(jiList):
        if (line_words+len(val) > 10) and i < 11:
            xPos = getMidPos(ji, width, 45) #30pt 微软雅黑字体 约等于 34 pixel
            draw.text((xPos,Ypos),ji,color,font=font)
            Ypos += 45
            ji = jiList[i] + ' '
            line_words = len(val)
        elif i < 14:
            line_words += len(jiList[i])
            ji += jiList[i] + ' '

    xPos = getMidPos(ji, width, 45) #30pt 微软雅黑字体 约等于 34 pixel
    draw.text((xPos,Ypos),ji ,color,font=font)
    #---------------------------------------------------------
    #保存图片
    try:
        im1.save(out_path + file_name,quality=100)
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

def checkPath(input_path):
    if input_path == "":
        return
    else:
        if not os.path.exists(input_path):
            print("文件夹不存在,创建文件夹：\n")
            os.makedirs(input_path)

def test():
    # ----------------------------------------------------------测试星座图片修改
    # img_path = "C:\\Users\\Andy\\Pictures\\1.jpg"
    # font = ImageFont.truetype("msyhbd.ttc",55,encoding='utf8')
    # im1 = Image.open(img_path)
    # draw = ImageDraw.Draw(im1)
    # draw.text((550,300),'搭理 我' ,(255,255,255),font=font)
    # im1.save("test.jpg")

    # ----------------------------------------------------------测试黄历
    print(datetime.now().strftime("%Y-%m-%d").split('-')[0])



def main():
    subprocess.call("",shell=True) #颜色
    checkPath(cons_path) #判断路径是否存在，如果不存在创建
    checkconsPath(cons_save)
    cons_result = consImages() # 星座function
    checkPath(huangli_save)
    h_result = huangli(tomorrow,huangli_path, huangli_save,tomorrow_list[0] + tomorrow_list[1]+tomorrow_list[2]+ "-" +"01.jpg")    # 黄历function
    h_result2 = huangli(tomorrow_after,huangli_path2, huangli_save,tomorrow_list[0] + tomorrow_list[1]+tomorrow_list[2]+ "-" + "02.jpg")    # 黄历function
    countDown = 0
    while countDown < auto_close:
        print("\033[1;31;40m"+str(auto_close-countDown)+"\033[0;40m秒后自动关闭", end="\r")
        sleep(1)
        countDown += 1
    # test()

if __name__ == '__main__':
    main()
