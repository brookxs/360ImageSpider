# -*- coding: utf-8 -*-
"""
批量采集360大图到本地
基于python2.7.x开发, 兼容python3
作者: brooks
微信公众号: 布鲁的python
"""
import os
import time
import requests

# 自定义请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
}


def get_images(cat, subcat, pn=0, retries=3):
    """
    获取图片数据
    :param cat: 要获取的图片分类
    :param subcat: 子分类id
    :param pn: 页码
    :param retries: 失败重试次数
    :return: json数据
    """
    url = "http://image.so.com/zj"
    params = {
        "ch": cat,
        "t1": subcat,
        "width": 1920,  # 图片宽度
        "height": 1200,  # 图片高度
        "sn": pn,
        "listtype": "new",
        "temp": 1
    }
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
    except requests.RequestException:
        data = None
        if retries > 0:
            return get_images(cat, pn, retries - 1)
    else:
        try:
            data = resp.json()
        except ValueError:
            data = None
    return data


def extract_and_download(data):
    """
    提取和下载图片
    :param data: 要提取的json数据
    :return: None
    """
    data_list = data.get("list", [])
    for item in data_list:
        width = item.get("cover_width", 0)
        height = item.get("cover_height", 0)
        imgurl = item.get("qhimg_url")
        # 只下载图片宽度大于1600 高度大于1000的图片
        if imgurl and width > 1600 and height > 1000:
            filename = imgurl.split("/")[-1]
            print(u"正在下载图片", filename)
            recive = requests.get(imgurl, headers=HEADERS)
            with open(filename, "wb") as imgfile:
                imgfile.write(recive.content)
        else:
            print(u"获取不到图片地址或图片大小不符合要求")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder_name = "images"
    folder_path = os.path.join(base_dir, folder_name)
    if not os.path.exists(folder_path):
        print(u"创建文件夹")
        os.mkdir(folder_path)
    print(u"切换程序运行目录")
    os.chdir(folder_path)

    # 分类名称
    catname = "wallpaper"
    # 子分类id
    subcatid = 157
    # 要采集的页数，每页30张
    num = 1

    for sn in range(num):
        print (u"开始爬取{}分类第{}页图片".format(catname, sn + 1))
        img_data = get_images(catname, sn)
        if img_data is None:
            print(u"抓取出错")
            continue
        extract_and_download(img_data)
        time.sleep(2)

    print(u"全部采集完毕")

