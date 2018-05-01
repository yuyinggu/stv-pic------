import os
from datetime import datetime,timedelta
from PIL import ImageFont, Image, ImageDraw

today = (datetime.now()).strftime("%Y-%m-%d") # 加 '+ timedelta(days=1)' 在now()后面测试明天的
tomorrow = (datetime.now()+ timedelta(days=1)).strftime("%Y-%m-%d")
today_list = today.split("-")
tomorrow_list = tomorrow.split("-")
tomorrow_after = (datetime.now()+ timedelta(days=2)).strftime("%Y-%m-%d")
tomorrow_after_list = tomorrow_after.split("-")

cons_path = "\\\\vdisk.chineseradio.local\\it\\Jobs\\Constellation\\Photo\\"#"C:\\Users\\helen.gu\\Documents\\GitHub\\stv-pic------\\" #星座背景文件夹路径（不含文件名）
cons_save = "\\\\vdisk.chineseradio.local\\VideoWork\\OtherVideos\\STPlayer\\Source\\"+ tomorrow_list[0]+"\\"+ tomorrow_list[1] +"\\"+ tomorrow_list[2] +"\\"+"Constellation/" #星座保存文件夹路径(不含文件名)
font_dir = "\\\\vdisk.chineseradio.local\\it\\Jobs\\Constellation\\Photo\\"#"C:\\Users\\helen.gu\\Documents\\GitHub\\stv-pic------\\"
constellation_txt = "\\\\vdisk.chineseradio.local\\VideoWork\\OtherVideos\\STPlayer\\Source\\"+ tomorrow_list[0]+"\\"+ tomorrow_list[1] +"\\"+ tomorrow_list[2] +"\\"+ tomorrow_list[1] + tomorrow_list[2] + "constellation" + ".txt" #txt文件路径

if not os.path.exists(constellation_txt):
    print("星座txt不存在")
    exit()

cons_list = ["摩羯座","水瓶座","双鱼座","白羊座","金牛座","双子座","巨蟹座","狮子座","处女座","天秤座","天蝎座","射手座"]


for i,cons in enumerate(cons_list):
    with open(constellation_txt, "r", encoding="utf8") as txt_file:
        result = txt_file.readlines()
        index = result.index(cons+"\n")
        content = result[index+1][:-1]

    # 分行
    temp = ""
    rows_count = 1
    for j in range(len(content)):
        if j % 13 == 0 and j != 0: #每行13字
            temp += ' \n' + content[j]
            rows_count += 1
        elif j == 13 * 7 -1:       #替换第七行 第十三个字 为 ...
            temp += '...'
            break
        else:
            temp += content[j]

    print(temp)

    # 生成图片
    img_path = cons_path + cons_list[i] + ".jpg"
    try:
        font = ImageFont.truetype(font_dir+"msyhbd.ttc",65,encoding='unic')
    except:
        input("\033[1;31;40m字体文件不存在\n")
        exit()
    try:
        im1 = Image.open(img_path)
    except OSError as e:
        input("\n\033[1;31;40m星座图片不存在或路径不对: " + e.strerror + "\033[0;40m")
        exit()
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
        exit()
    print("\n\033[1;32;40m%s图片生成成功\n\033[0;40m" % cons)
