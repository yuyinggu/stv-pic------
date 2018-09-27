import os
from PIL import Image
import piexif
from subprocess import Popen

files_path = r'G:\News'     # 文件根路径
files_list = sorted(os.listdir(files_path), reverse=True)   # 文件列表 倒序
txt_dict = {}

for file in files_list:
    file_name, file_extension = file.split('.')
    if file_extension == 'txt':
        # print(file)
        txt_dict[file_name] = []
    if file_extension == ('jpg' or 'jpeg'):
        # print(file)
        jpg_prefix = file_name.split('-')[0]
        # print(jpg_prefix)
        if jpg_prefix in txt_dict:
            # print(file)
            txt_dict[jpg_prefix].append(file)

# print(txt_dict)

for txt_name, img_list in txt_dict.items():
    # 把txt转换成 utf8 格式
    txt_file_path = os.path.join(files_path, txt_name + '.txt')
    f = open(txt_file_path, 'rb+')
    content = f.read()
    try:
        new_utf8_content = content.decode('big5').encode('utf8')
        f.truncate(0)
        f.seek(0, 0)
        f.write(new_utf8_content)
        f.close()
    except:
        f.close()
        pass

    print(txt_name, img_list)
          # ,content)

    for img_name in img_list:
        # -XPSubject    分类
        # -XPTitle      标题
        exiftool_proc = Popen('exiftool.exe -overwrite_original "-XPSubject<={0}" "-XPTitle<={1}" {2}'.format(
            txt_file_path,
            txt_file_path,
            os.path.join(files_path, img_name)))
        print(exiftool_proc.communicate()[0])

    # for img_name in img_list:
    #     img_path = os.path.join(files_path, img_name)
    #     img = Image.open(img_path)
    #     exif_dict = piexif.load(img.info['exif'])
    #     exif_dict["0th"][40092] = content.encode('utf-16')
    #     img.save(img_path, exif=piexif.dump(exif_dict))