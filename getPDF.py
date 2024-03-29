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

i=1
x=2
y=3
z=4

sql = "update tag set a = %d,b = %d,c = %d,d = %d"% (i,x,y,z)
cursor.execute(sql)
db.commit()  # 提交事务


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

for i in range(1,len(bigtype['data'])):
  #  print("开始爬取" + i['columnname'] + "，参数：" + i["columnid"])

    print (bigtype['data'][i]['columnid'])
    field_bigTypeCode = str(bigtype['data'][i]['columnid']).strip()
    curListHtml = parseHtml(getHtml("http://icid.iachina.cn/ICID/front/leafColComType.do?columnid=%s" % field_bigTypeCode,
                                    'GBK'))
    print("-------")
    curList = curListHtml.find_all("li", op_id="type_me")
    # 循环获取单条数据
    for j in range(0,len(curList)):
        print(curList[j].find("a").get("id"))
        break