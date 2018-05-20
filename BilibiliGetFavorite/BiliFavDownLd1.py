from urllib import request
from functools import reduce
from multiprocessing import Pool
import json,time,os

vmid = ""
fid = ""
data = []
videourl = "https://www.bilibili.com/video/av"
removechr = {"/": "-",
             "\\": "-",
             ":": "-",
             "*": "-",
             "?": "-",
             "<": "-",
             ">": "-",
             "|": "-",
             "：" : "-",
             "\"" : "-",
             "→" : "-"
            }
specialchr = {"\\u0026": "&",
              "\\u003c" : "<",
              "\\u003e" : ">"}

def rmvchr(s) :
    if s in removechr:
        return removechr[s]
    else:
        return s

def rplchr(s):
    for key, value in specialchr.items():
        s.replace(key,value)
    return s


def getdata(number):

    def tryget():
        try:
            wholeHTML = request.urlopen(wholeurl).read().decode("utf-8")
            jsondata = json.loads(wholeHTML)
        except:
            print("获取失败，暂停3秒")
            print("获取数据: 第%s个==>" % pn, end="")
            time.sleep(3)
            while True:
                try:
                    wholeHTML = request.urlopen(wholeurl).read().decode("utf-8")
                    jsondata = json.loads(wholeHTML)
                    break
                except:
                    print("获取失败，暂停3秒")
                    print("获取数据: 第%s个==>" % pn, end="")
                    time.sleep(3)
        return jsondata

    data = []
    for pn in range(number):
        pn += 1
        print("获取数据: 第%s个==>" % pn,end="")
        #格式化api
        wholeurl = apiurl % pn
        jsondata = tryget()
        code = jsondata["code"]
        if code == 0:
            print("获取成功",end="")
        else:
            print("返回值:%s,返回信息:%s" % (code, jsondata["message"]))
            while code != 0:
                print("获取数据: 第%s个==>" % pn, end="")
                jsondata = tryget()
                code = jsondata["code"]
            print("获取成功",end="")

        data.append({"aid":str(jsondata["data"]["archives"][0]["aid"]),
                     "title":str(jsondata["data"]["archives"][0]["title"]),
                     "pic":str(jsondata["data"]["archives"][0]["pic"])})
        print("------(AV号:%s,标题:%s)" % (data[pn-1]["aid"], data[pn-1]["title"]))
    return data

def download_by_aria2(data):
    #plz help me
    #i don't know how to do that
    pass

def download_by_lulu(data):

    expt = input("Export Data? y/n ")
    if expt == "y":
        with open(txtsave, "w", encoding="utf-8") as exfile:
            for video in data:
                # 标题使用替换特殊字符后的标题
                exfile.write((video["aid"] + "---" + rplchr(video["title"]) + "---" + video["pic"] + "\n"))
        print("Finish export data")
    else:
        print("Skip")

    downldpic = input("Download Covers? y/n ")
    if downldpic == "y":
        piclist = []
        for video in data:
            # 使用-代替特殊字符
            title = reduce(lambda x, y: x + y, map(rmvchr, video["title"]))
            piclist.append([title,video["pic"]])

        i = -1
        while i < len(piclist):
            p = Pool(4)
            for j in range(5):
                i += 1
                if i < len(piclist):
                    p.apply_async(
                        os.system(
                            "lulu --output-dir %s --output-filename '%s' %s" % (picsave, piclist[i][0], piclist[i][1])),
                        args=(i,))
            print('Waiting for 4 subprocesses done...')
            p.close()
            p.join()
            print('4 subprocesses done.')
        print("Finish download covers")
    else:
        print("Skip")

    downld = input("Download Video? y/n ")
    if downld == "y":
        videolist = []
        for video in data:
            # 使用-代替特殊字符
            title = reduce(lambda x, y: x + y, map(rmvchr, video["title"]))
            videolist.append([title, video["aid"]])
        i = -1
        while i < len(videolist):
            p = Pool(4)
            for j in range(5):
                i += 1
                if i < len(videolist):
                    p.apply_async(
                        os.system(
                            "lulu --output-dir %s --output-filename %s %s" % (picsave, videolist[i][0], videolist[i][1])),
                        args=(i,))
            print('Waiting for 4 subprocesses done...')
            p.close()
            p.join()
            print('4 subprocesses done.')
        print("Finish download video")
    else:
        print("Skip")

    return "finish"

if __name__=="__main__":
    #favlink = input("Enter Favorite Folder Link")
    favlink = "https://space.bilibili.com/10003632/#/favlist?fid=20677228/"
    #如果最后有/则去掉/
    if favlink[-1] == "/":
        favlink = favlink[:-1:]
    #获取vmid
    vmid = favlink[favlink.find("com", 0) + 4:favlink.find("/#", 0):]
    #获取fid
    fid = favlink[favlink.find("fid", 0) + 4::]
    #api链接
    apiurl = "https://api.bilibili.com/x/v2/fav/video?vmid=%s&ps=1&fid=%s&pn=%s" % (vmid, fid, "%s")
    #获取需要个数
    number = int(input("enter your number: "))
    #datasvrt = input("Enter data save route(full)")
    #imgsvrt = input("Enter image save route(full)")
    #videosvrt = input("Enter video save route(full)")
    txtsave = "E:\\Download\\export\\1.txt"
    picsave = "E:\\Download\\export\\img\\"
    videosave = "E:\\Download\\export\\video\\"

    data = getdata(number)
    download_by_lulu(data)