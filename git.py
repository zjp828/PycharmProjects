import urllib.request
from bs4 import BeautifulSoup
#连接mysql
import pymysql
#解析json
import demjson


db = pymysql.connect("localhost", "root", "123456", "pdftest")
cursor = db.cursor()

def getHtml(url, charset):
    # 获取网页内容
    page = urllib.request.urlopen(url)
    html = page.read()
    return html.decode(charset, "ignore")#设置为ignore，则会忽略非法字符；
# BeautifulSoup HTML/XML的解析器 支持多种选择器
def parseHtml(html):
    html = BeautifulSoup(html, "html.parser")
    return html


#获取大类
bigtype = getHtml(
    "http://icid.iachina.cn/ICID/front/getColumnsType.do",'utf-8')

bigtype = demjson.decode(str(bigtype))#将已编码的 JSON 字符串解码为 Python 对象


def getComType(var):
    # 类型对应编号
    typeList = {"01": "集团公司（控股公司）", "02": "财产险公司", "03": "人身险公司", "04": "资产管理公司", "05": "再保险公司"}.get(var,'error')
    return typeList

def getFile(url,pdfname):
    file_name = "D:\\pdf\\"+pdfname
    u = urllib.request.urlopen(url)

    f = open(file_name, 'wb')
    block_sz = 8192#下载大文件
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        f.write(buffer)
    f.close()
    print ("Sucessful to download" + " " + file_name)


# 公司大类
field_bigType = ""
# 公司大类代码
field_bigTypeCode = ""
# 公司类型
field_companyType = ""
# 公司类型代码
field_companyTypeCode = ""
# 公司全名
field_companyAllName=""
# 公司全名代码
field_companyAllNameCode=""
# 信息标题
field_informationTitle=""
# 信息标题代码
field_informationTitleCode=""
# 发布时间
field_createTime=""
# 中文名称
field_PDFname=""
# 唯一id标识
field_PDFid=""

try:
    for i in bigtype['data']:
        print("开始爬取"+i['columnname']+",参数"+i['columnid'])
        field_bigType = str(i['columnname']).strip()
        field_bigTypeCode = str(bigtype['data'][i]['columnid']).strip()
        # 获取一个类型
        curListHtml = parseHtml(getHtml("http://icid.iachina.cn/ICID/front/leafColComType.do?columnid=%s" % field_bigTypeCode,
                             'GBK'))
        print("-------")
        curList = curListHtml.find_all("li",op_id="type_me")
        # 循环获取单条数据
        for j in curList:
            param = j.find("a").get("id")
            if param != None:
                print(param, j.find("a").get_text())
                type_code = j.get("type_code")
                # 保存数据库字段——公司类型代码
                field_companyTypeCode = str(type_code).strip()
                # 保存数据库字段——公司类型
                field_companyType = str(getComType(type_code)).strip()
                # 保存数据库字段——公司全名代码
                field_companyAllNameCode = str(param).strip()
                # 保存数据库字段——公司全名
                field_companyAllName = str(j.find("a").get_text()).strip()

                #pdf列表页面
                curItemUrl="http://icid.iachina.cn/ICID/front/getCompanyInfos.do?columnid=%s&comCode=%s&attr=01" % (field_bigTypeCode, param)
                curItemList = parseHtml(getHtml(curItemUrl, "GBK")).find("div", class_="jie_nei").find_all("li")
                for x in curItemList:
                    # 保存数据库字段——信息标题
                    field_informationTitle = x.find("a").get_text()
                    # 保存数据库字段——信息标题代码
                    field_informationTitleCode =  x.find("a").get("id")
                    # 保存数据库字段——发布时间
                    field_createTime = x.find("p", class_="kk").get_text()

                    curItemUrl1 = "http://icid.iachina.cn/ICID/front/infoDetail.do?informationno=%s" % str(
                        field_informationTitleCode)
                    pdfhtml = parseHtml(getHtml(curItemUrl1, "GBK")).find("div", class_="pdf_a").find_all("li")

                    for z in  pdfhtml:
                        if z < 1:
                            continue
                        # 保存数据库字段——信息id
                        field_PDFid = z.find("a").get("id").strip()

                        pdfurl = "http://icid.iachina.cn/ICID/files/piluxinxi/pdf/" + field_PDFid

                        pdfname = z.find("a").get_text().strip()
                        # 保存数据库字段——pdf文件名
                        field_PDFname = pdfname
                        # 数据库操作sql
                        sql = "insert into pdf (field_bigType,field_bigTypeCode,field_companyType,field_companyTypeCode,field_companyAllName,field_companyAllNameCode," \
                              "field_informationTitle,field_informationTitleCode,field_PDFid,field_PDFname,field_createTime)VALUES ('%s','%s','%s','%s','%s'," \
                              "'%s','%s','%s','%s','%s','%s')" % (field_bigType,field_bigTypeCode, field_companyType,field_companyTypeCode,field_companyAllName,
                              field_companyAllNameCode,field_informationTitle,field_informationTitleCode,field_PDFid,field_PDFname,field_createTime)
                        print(sql)
                        cursor.execute(sql)
                        print(pdfurl)
                        print("开始下载。。。")
                        getFile(pdfurl, field_PDFid)
                        print(pdfname + "已保存")
                        db.commit()  # 提交事务
                        print(i,j,x,z)
except Exception as e:
    db.rollback()
    raise e # 抛出错误