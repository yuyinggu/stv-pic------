import os
from PIL import ImageFont, Image, ImageDraw
from datetime import datetime,timedelta

today = (datetime.now()).strftime("%Y-%m-%d") # 加 '+ timedelta(days=1)' 在now()后面测试明天的
tomorrow = (datetime.now()+ timedelta(days=1)).strftime("%Y-%m-%d")
today_list = today.split("-")
tomorrow_list = tomorrow.split("-")
tomorrow_after = (datetime.now()+ timedelta(days=2)).strftime("%Y-%m-%d")
tomorrow_after_list = tomorrow_after.split("-")

huangli_path = "/Users/andymao/Documents/stv-pic------/黃曆_Background-01.jpg"#"\\\\vdisk.chineseradio.local\\it\\Jobs\\Constellation\\Photo\\Background-01.jpg" #黄历背景图片路径
huangli_path2 = "/Users/andymao/Documents/stv-pic------/黃曆_Background-02.jpg"##"\\\\vdisk.chineseradio.local\\it\\Jobs\\Constellation\\Photo\\Background-02.jpg" #黄历背景图片路径
huangli_save = "/Users/andymao/Documents/stv-pic------/"##"\\\\vdisk.chineseradio.local\\VideoWork\\OtherVideos\\STPlayer\\Source\\"+ tomorrow_list[0]+"\\"+ tomorrow_list[1] +"\\"+ tomorrow_list[2] +"\\"+"SideAd/" #黄历输出图片路径
huangli_txt = "/Users/andymao/Documents/stv-pic------/huangli.txt"##"\\\\vdisk.chineseradio.local\\VideoWork\\OtherVideos\\STPlayer\\Source\\"+ tomorrow_list[0]+"\\"+ tomorrow_list[1] +"\\"+ tomorrow_list[2] +"\\"+ tomorrow_list[1] + tomorrow_list[2] + "huangli" + ".txt" #txt文件路径
font_dir = "/Users/andymao/Documents/stv-pic------/"##"\\\\vdisk.chineseradio.local\\it\\Jobs\\Constellation\\Photo\\"#"C:\\Users\\helen.gu\\Documents\\GitHub\\stv-pic------\\"

if not os.path.exists(huangli_txt):
    print("黄历txt不存在")
    exit()


def getMidPos(string, width, pixel_word):
    wordsCount = 0
    for val in string.split(" "):
        wordsCount += len(val)
    xPos = (width/2)-((wordsCount*pixel_word)/2)
    return xPos

# 生成黄历图片
def huangli(day,in_path,out_path,file_name):
    with open(huangli_txt, "r", encoding='utf8') as txt_file:
        result = txt_file.readlines()
        index = result.index(day+"\n")
        yinli = result[index+1][:-1]
        yi = result[index+3][:-1]
        ji = result[index+5][:-1]

    print("阴历: "+yinli + "\n宜:\t"+ yi + "\n吉:\t"+ji)

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
    # 农历 yinli
    # "甲午(马)年八月十八"

    xPos = getMidPos(yinli, width, 35) #35pt 微软雅黑字体 约等于 40 pixel
    font = ImageFont.truetype(font_dir+"msyhbd.ttc",40,encoding='unic')
    draw.text((xPos,210),yinli ,color,font=font)

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
        elif i < 12:     #最后一行 字数
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
        elif i < 12:    #最后一行 字数
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
    else:
        print("\n\033[1;32;40m黄历图片生成成功\n\033[0;40m")


huangli(tomorrow,huangli_path, huangli_save,tomorrow_list[0] + tomorrow_list[1]+tomorrow_list[2]+ "-" +"01.jpg")    # 黄历function
huangli(tomorrow_after,huangli_path2, huangli_save,tomorrow_list[0] + tomorrow_list[1]+tomorrow_list[2]+ "-" + "02.jpg")    # 黄历function
