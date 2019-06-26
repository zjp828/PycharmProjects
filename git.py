# encoding=utf8
import urllib.request
from bs4 import BeautifulSoup
#连接mysql
import pymysql
#解析json
import demjson

db = pymysql.connect("localhost", "root", "123456", "pdfTest")
cursor = db.cursor()


def getHtml(url, charset):
    # 获取网页内容
    page = urllib.request.urlopen(url)
    html = page.read()
    return html.decode(charset, "ignore")


def parseHtml(html):
    html = BeautifulSoup(html, "html.parser")
    return html


url = "http://icid.iachina.cn/ICID/front/getColumnsType.do"
# 获取大类
bigType = getHtml(url, "utf-8")
bigType = demjson.decode(str(bigType))

# 类型对应编号
typeList = {"01": "集团公司（控股公司）", "02": "财产险公司", "03": "人身险公司", "04": "资产管理公司", "05": "再保险公司"}

# 要插入数据库的字段
field_bigType = ""

field_companyType = ""

field_companyAllName=""

field_informationTitle=""

field_createTime=""

field_PDFname=""

for i in bigType['data']:
    print("开始爬取" + i['columnname'] + "，参数：" + i["columnid"])

    # 获取一个类型
    curListUrl = "http://icid.iachina.cn/ICID/front/leafColComType.do?columnid=%s" % i["columnid"]
    curListHtml = parseHtml(getHtml(curListUrl, "GBK"))
    curList = curListHtml.find_all("li", op_id="type_me")
    # 循环获取单条数据
    for j in curList:
        param = j.find("a").get("id")
        if param != None:
            print(param, j.find("a").get_text())
            curItemUrl = "http://icid.iachina.cn/ICID/front/getCompanyInfos.do?columnid=%s&comCode=%s&attr=01" % (i["columnid"], param)
            curItemList = parseHtml(getHtml(curItemUrl, "GBK")).find("div", class_="jie_nei").find_all("li")
            for x in curItemList:
                curItemUrl1 ="http://icid.iachina.cn/ICID/front/infoDetail.do?informationno=%s" % str(x.find("a").get("id"))
                pdfhtml= parseHtml(getHtml(curItemUrl1, "GBK")).find("div", class_="pdf_a").find_all("li")
                for b in pdfhtml:
                    pdfurl = b.find("a").get("id")
                    pdfname = b.find("a").get_text()
                    print(pdfurl, pdfname)