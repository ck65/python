# -*- coding: UTF-8 -*-
import urllib2
import re
import MySQLdb
import StringIO, gzip
import bs4
import chardet


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
        sql = "INSERT INTO ctf_info(Name, Data, Fromat, Location, Note) VALUE (%s, %s, %s, %s, %s)" % (self.Name, self.Date, self.Format, self.Location, self.Notes)
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()

url = "https://ctftime.org/event/oldlist/upcoming"
# url="https://www.baidu.com"
res = urllib2.Request(url)
res.add_header("authority ", "ctftime.org")
res.add_header("method", "GET")
res.add_header("path", "/event/oldlist/upcoming")
res.add_header("scheme", "http")
res.add_header("accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8")
res.add_header("accept-encoding", "gzip, deflate, br")
res.add_header("accept-language", "zh-CN,zh;q=0.9,en;q=0.8")
res.add_header("cookie", "__utma=225924040.847076043.1544581453.1544581453.1544581453.1; __utmc=225924040; "
                         "__utmz=225924040.1544581453.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=("
                         "not%20provided); __utmt=1; _ym_uid=1544581454340783893; _ym_d=1544581454; _ym_isad=1; "
                         "_ym_visorc_14236711=w; __atuvc=1%7C50; __atuvs=5c1072dcfa5c83ab000; "
                         "__utmb=225924040.10.10.1544581453")
res.add_header("referer", "https://ctftime.org/event/oldlist/upcoming")
res.add_header("upgrade-insecure-requests", "1")
res.add_header("user-agent",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36")
html = urllib2.urlopen(res)


def gzdecode(data):
    compressedstream = StringIO.StringIO(data)
    gziper = gzip.GzipFile(fileobj=compressedstream)
    data2 = gziper.read()  # 读取解压缩后数据
    return data2


print str(html.getcode())
# print len(html.read())
s = html.read()
print chardet.detect(s)
s = gzdecode(s)


# with open("1.html","w+") as f:
# f.write(s)
# print s
def chose(links):
    flag = []
    for i in range(len(links)):
        sd = str(links[i])
        sr = re.compile(r'<[^>]+>', re.S)
        sd = sr.sub('', sd)
        if (sd == '') | (sd == '\n'):
            continue
        flag.append(sd.strip())
    return flag


def connect_db(user, password):
    db = MySQLdb.connect("localhost", user, password, "ctf", charset='utf8')
    return db


if html.getcode() == 200:
    soup = bs4.BeautifulSoup(s, 'lxml')
    links = soup.findAll('td')
    info = chose(links)
    i = 0
    while i < (len(info)-4):
        if info[i] == "SOC Battle":
            s1 = game(info[i], info[i + 1], info[i + 2], "none", info[i + 3])
            i = i + 4
        else:
            s1 = game(info[i], info[i + 1], info[i + 2], info[i + 3], info[i + 4])
            i = i + 5
        s1.show()
        db = connect_db("root", "root")
        s1.insert_db(db)
        db.close()
