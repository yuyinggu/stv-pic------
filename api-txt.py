import os
from opencc import OpenCC
import json
from urllib.request import urlopen
from urllib.parse import urlencode
from datetime import datetime,timedelta

today = (datetime.now()).strftime("%Y-%m-%d") # 加 '+ timedelta(days=1)' 在now()后面测试明天的
tomorrow = (datetime.now()+ timedelta(days=1)).strftime("%Y-%m-%d")
today_list = today.split("-")
tomorrow_list = tomorrow.split("-")
tomorrow_after = (datetime.now()+ timedelta(days=2)).strftime("%Y-%m-%d")
tomorrow_after_list = tomorrow_after.split("-")

cons_save = "\\\\vdisk.chineseradio.local\\VideoWork\\OtherVideos\\STPlayer\\Source\\"+ tomorrow_list[0]+"\\"+ tomorrow_list[1] +"\\"+ tomorrow_list[2] +"\\"+"Constellation/" #星座保存文件夹路径(不含文件名)
huangli_save = "\\\\vdisk.chineseradio.local\\VideoWork\\OtherVideos\\STPlayer\\Source\\"+ tomorrow_list[0]+"\\"+ tomorrow_list[1] +"\\"+ tomorrow_list[2] +"\\"+"SideAd/" #黄历输出图片路径
openCC = OpenCC('s2t')
constellation_txt = "\\\\vdisk.chineseradio.local\\VideoWork\\OtherVideos\\STPlayer\\Source\\"+ tomorrow_list[0]+"\\"+ tomorrow_list[1] +"\\"+ tomorrow_list[2] +"\\"+ tomorrow_list[1] + tomorrow_list[2] + "constellation" + ".txt" #txt文件路径
huangli_txt = "\\\\vdisk.chineseradio.local\\VideoWork\\OtherVideos\\STPlayer\\Source\\"+ tomorrow_list[0]+"\\"+ tomorrow_list[1] +"\\"+ tomorrow_list[2] +"\\"+ tomorrow_list[1] + tomorrow_list[2] + "huangli" + ".txt" #txt文件路径


def checkPath(input_path):
    if input_path == "":
        return
    else:
        if not os.path.exists(input_path):
            print("文件夹不存在,创建文件夹：\n")
            os.makedirs(input_path)

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

        with open(constellation_txt,"a",encoding='utf-8') as txt_file:
            print(cons + '\n', openCC.convert(res["summary"]))
            txt_file.write(cons+"\n")
            txt_file.write(openCC.convert(res["summary"])+"\n")
            txt_file.close()
    except:
        print("\n无法拿到星座")

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

    yinli = openCC.convert(res["result"]["yinli"]) #阴历
    jishen = openCC.convert(res["result"]["jishen"]) #吉神
    xiongshen = openCC.convert(res["result"]["xiongshen"]) #凶神
    yi = openCC.convert(res["result"]["yi"]) #宜
    ji = openCC.convert(res["result"]["ji"]) #忌

    print("阴历: "+yinli + "\n吉神:\t"+jishen + "\n凶神:\t"+xiongshen + "\n宜:\t"+ yi + "\n吉:\t"+ji)
    
    with open(huangli_txt,"a",encoding='utf8') as txt_file:
        txt_file.write(day+"\n")
        txt_file.write(yinli+"\n")
        txt_file.write("宜"+"\n")
        txt_file.write(yi+"\n")
        txt_file.write("忌"+"\n")
        txt_file.write(ji+"\n")
        txt_file.close()


def main():
    # 星座 API
    checkPath(cons_save)
    checkPath(huangli_save)
    cons_list = ["摩羯座","水瓶座","双鱼座","白羊座","金牛座","双子座","巨蟹座","狮子座","处女座","天秤座","天蝎座","射手座"]
    #cons_list2 = ["mojie","shuiping","shuangyu","baiyang","jinniu","shuangzi","juxie","shizi","chunv","tiancheng","tianxie","sheshou"]
    for i,cons in enumerate(cons_list):
        getConstellation(cons)

    # 黄历 API

    get_huangli(tomorrow)
    get_huangli(tomorrow_after)


if __name__ == '__main__':
    main()
