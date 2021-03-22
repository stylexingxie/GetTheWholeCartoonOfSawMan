import re
from bs4 import BeautifulSoup
import os
import base64
import requests
import urllib.request

pre_path = 'write your local path here'


def mkdir(index):
    path_pre = pre_path
    index = str(index)
    path = os.path.join(path_pre, index)
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    return os.path.join(path, '')

# The url link is quoted from the "Saw Man" offical account
# and is for learning and research only
# and cannot be used for various commercial purposes.

def getAllUrl():
    url = 'https://mp.weixin.qq.com/s/3z000CvW3LwkvEr7IBMGgg'
    # r=requests.get(url)
    # soup=BeautifulSoup(r.text,"lxml")
    # titles=soup.select('#js_content > p')
    # for title in titles:
    #     print(title)

    pattern1 = '<.*?(href=".*?").*?'

    headers = {'User-Agent',
               'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    data = opener.open(url).read().decode('utf8')

    content_href = re.findall(pattern1, data, re.I)
    # print(content_href)
    # print(type(content_href))
    # print(content_href[11:-7])
    content_href = content_href[11:-7]
    url_list = []
    for url_conf in content_href:
        temp = url_conf.split('"')
        # print(type(temp))
        # print(len(temp))
        # print(temp[1])
        url_list.append(temp[1])
    # print(url_list)
    return url_list


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def getimgURL(html):
    soup = BeautifulSoup(html, "html.parser")
    adlist = []
    for i in soup.find_all("img"):
        try:
            ad = re.findall(r'.*src="(.*?)?" .*', str(i))
            if ad:
                # if ad.startswith('https://mmbiz.qpic.cn/'):
                # print(type(ad[0]))
                if ad[0].startswith('https://mmbiz.qpic.cn/'):
                    adlist.append(ad)
        except:
            continue
    return adlist


def getImage(url_list):
    p = 1
    for uurrll in url_list:
        print(uurrll)
        path = mkdir(p)
        html = getHTMLText(uurrll)
        list = getimgURL(html)
        for i in range(len(list)):
            ppath = path + str(i) + "." + 'png'
            print(ppath)
            r = requests.get(list[i][0])
            with open(ppath, 'wb') as f:
                f.write(r.content)
                f.close()
        p += 1


# getImage()


if __name__ == '__main__':
    url_list = getAllUrl()
    getImage(url_list)
