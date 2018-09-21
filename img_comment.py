import os
from PIL import Image
import piexif

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
for key, img_list in txt_dict.items():
    with open(os.path.join(files_path, key + '.txt'), 'r', encoding='big5', errors='ignore') as f:
        # print(key)
        content = str(f.read())
        f.close()
    print(key, img_list, content)
    for img_name in img_list:
        img_path = os.path.join(files_path, img_name)
        img = Image.open(img_path)
        exif_dict = piexif.load(img.info['exif'])
        exif_dict["0th"][40092] = content.encode('utf-16')
        img.save(img_path, exif=piexif.dump(exif_dict))