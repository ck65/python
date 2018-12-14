# -*- coding: UTF-8 -*-
import urllib2
import re
import MySQLdb
import StringIO
import gzip
import bs4


class game:
    Name = ""
    Date = ""
    Format = ""
    Location = ""
    Notes = "none"

    def __init__(self, name, data, format, location, notes):
        self.Date = data
        self.Format = format
        self.Name = name
        self.Notes = notes
        self.Location = location

    def show(self):
        print "Name: " + self.Name + "\nDate: " + self.Date + "\nFormat: " + self.Format + "\nLocation: " + self.Location + "\nNote: " + self.Notes + "\n"

    def insert_db(self, db):
        sql = "INSERT INTO ctf_info(Name, Data, Fromat, Location, Note) VALUE (\"%s\",\" %s\", \"%s\", \"%s\",\" %s\");" % (
            self.Name, self.Date, self.Format, self.Location, self.Notes)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

    def insert_dbx(self, db):
        sql = "INSERT INTO xctf(name, Format, Location, Data, Statue)  VALUE (\"%s\",\" %s\", \"%s\", \"%s\",\" %s\");" % (
            self.Name, self.Format, self.Date, self.Location, self.Notes)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()


class team:
    No = 0
    Name = ""
    Sco = 0

    def __init__(self, no, name, soc):
        self.No = no
        self.Name = name
        self.Sco = soc

    def insert_dbx(self, db):
        sql = "INSERT INTO team(No, Name, Soc) VALUE (\"%d\",\"%s\",\"%d\")" % (self.No, self.Name, self.Sco)
        cour = db.cursor()
        try:
            cour.execute(sql)
            db.commit()
        except:
            db.rollback()


class urls:
    url = ""
    result = ""
    info = ""
    game = []
    links = ""

    def __init__(self, url):
        self.url = url;

    def int(self):
        res = urllib2.Request(self.url)
        res.add_header("authority ", "ctftime.org")
        res.add_header("method", "GET")
        res.add_header("path", "/event/oldlist/upcoming")
        res.add_header("scheme", "http")
        res.add_header("accept",
                       "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
        res.add_header("accept-encoding", "gzip, deflate, br")
        res.add_header("accept-language", "zh-cn,zh;q=0.9,en;q=0.8")
        res.add_header("cookie", "__utma=225924040.847076043.1544581453.1544581453.1544581453.1; __utmc=225924040; "
                                 "__utmz=225924040.1544581453.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=("
                                 "not%20provided); __utmt=1; _ym_uid=1544581454340783893; _ym_d=1544581454; _ym_isad=1; "
                                 "_ym_visorc_14236711=w; __atuvc=1%7C50; __atuvs=5c1072dcfa5c83ab000; "
                                 "__utmb=225924040.10.10.1544581453")
        res.add_header("referer", "https://ctftime.org/event/oldlist/upcoming")
        res.add_header("upgrade-insecure-requests", "1")
        res.add_header("user-agent",
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36")
        self.result = urllib2.urlopen(res).read()
        self.gzdecode()

    def int2(self):
        res = urllib2.Request(self.url)
        res.add_header("Accept",
                       "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
        res.add_header("Accept-Encoding", "gzip, deflate, br")
        res.add_header("accept-language", "zh-cn,zh;q=0.9,en;q=0.8")
        res.add_header("Cache-Control", "max-age=0")
        res.add_header("Connection", "keep-alive")
        res.add_header("Cookie",
                       "Hm_lvt_280598fde84b5357eb1d6226ac60f1f6=1542988284,1543305939,1544694257; csrftoken=ZFY3ClAZn2ZDLinUiBQ4UEAo5Rs8OyvoXgkKch9csDuymycHCGFajATaUhOtp9ub; sessionid=lh6qx3fjt68xvb438e8g7sxvpccz3unt; Hm_lpvt_280598fde84b5357eb1d6226ac60f1f6=1544694415")
        res.add_header("Host", "www.xctf.org.cn")
        res.add_header("Referer", "https://www.xctf.org.cn/ctfs/all/")
        res.add_header("Upgrade-Insecure-Requests", "1")
        res.add_header("User-Agent",
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36")
        self.result = urllib2.urlopen(res).read()

    def gzdecode(self):
        compressedstream = StringIO.StringIO(self.result)
        gziper = gzip.GzipFile(fileobj=compressedstream)
        self.result = gziper.read()  # 读取解压缩后数据

    def chose(self):
        flag = []
        for i in range(len(self.links)):
            sd = str(self.links[i])
            sr = re.compile(r'<[^>]+>', re.S)
            sd = sr.sub('', sd)
            if (sd == '') | (sd == '\n'):
                continue
            flag.append(sd.strip().replace(",", " ").decode("utf-8"))
        return flag

    def getinfo(self, th):
        soup = bs4.BeautifulSoup(self.result, "lxml")
        self.links = soup.find_all(th)
        self.game = self.chose()
        return self.game


url = "https://ctftime.org/event/oldlist/upcoming"
Xctf = "https://www.xctf.org.cn/ctfs/recently/"


def connect_db(user, password):
    db = MySQLdb.connect(host="127.0.0.1", user=user, passwd=password, db="ctf", charset='GBK')
    return db


if __name__ == '__main__':
    ctftime = urls(url)
    xctf = urls(Xctf)
    xctf.int2()
    ctftime.int()
    info = ctftime.getinfo("td")
    info2 = xctf.getinfo("span")
    flag = 0
    for d in info2:
        print d
    i = 0
    db = connect_db("root", "root")
    while i < (len(info) - 4):
        if info[i] == "SOC Battle":
            s1 = game(info[i], info[i + 1], info[i + 2], "none", info[i + 3])
            i = i + 4
        else:
            s1 = game(info[i], info[i + 1], info[i + 2], info[i + 3], info[i + 4])
            i = i + 5
        # s1.show()
        s1.insert_db(db)
    db.close()
    db = connect_db("root", "root")
    i = 1
    while True:
        if i > len(info2) - 7:
            break
        if i == 51:
            i = i + 1
            continue
        if i > 51:
            s2 = team(int(info2[i]), info2[i + 1], float(info2[i + 2]))
            i = i + 4
        elif i < 51:
            s2 = game(info2[i], info2[i + 1], info2[i + 2], info2[i + 3], info2[i + 4])
            i = i + 5
        # s2.show()
        s2.insert_dbx(db)
    db.close()
