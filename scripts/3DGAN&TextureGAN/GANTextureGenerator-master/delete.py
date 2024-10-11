import os
import glob

# 指定目录
directory = './u'

# 获取指定目录中所有后缀名为".png"的文件列表
png_files = glob.glob(os.path.join(directory, "*.png"))

# 遍历文件列表，逐个删除文件
for png_file in png_files:
    try:
        os.remove(png_file)
        print(f"已删除文件：{png_file}")
    except OSError as e:
        print(f"删除文件时出错：{e}")
