import urllib.request
from bs4 import BeautifulSoup
#连接mysql
import pymysql
#解析json
import demjson

import random

db = pymysql.connect("localhost", "root", "123456", "pdd")
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
    file_name = "D:\\pdd\\"+pdfname

    ua = [
        "UCWEB7.0.2.37/28/999",
        "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "Opera/8.0 (Windows NT 5.1; U; en)",
        "Openwave/ UCWEB7.0.2.37/28/999",
        "NOKIA5700/ UCWEB7.0.2.37/28/999",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1 Fennec/7.0a1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ",
        "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.1812",
        "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; Redmi 3S Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.3 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; Redmi 3S Build/MMB29M) AppleWebKit/533.1 (KHTML, like Gecko) Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.",
        "Mozilla/5.0 (Linux; Android 6.0.1; Redmi 3S Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043124 Safari/537.36 MicroMessenger/6.5.7.1041 NetType/WIFI Language/zh_CN",
        "Mozilla/5.0 (Linux; Android 6.0.1; Redmi 3S Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.94 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-N9200 Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.4 Chrome/38.0.2125.102 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 4.4.4; en-us; Nexus 5 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2307.2 Mobile Safari/537.36",
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3 XiaoMi/MiuiBrowser/8.7.0",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER) ",
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
        "JUC (Linux; U; 2.3.7; zh-cn; MB200; 320*480) UCWEB7.9.3.103/139/999",
        "Dalvik/2.1.0 (Linux; U; Android 6.0.1; Redmi 3S MIUI/7.3.9)",
        "Dalvik/1.6.0 (Linux; U; Android 4.4; Nexus 5 Build/KRT16M)",
    ]

    headers = {"User-Agent": random.choice(ua),
               "Cookie": "JSESSIONID=A5A0AAC102457D188A8413603E5D8323; acw_tc=65c86a0a15610973292931364edbca7c6425099e84ce01c24cd7c969d2308c; _pk_ses.6.1152=1; SERVERID=e058fcfed3b7b21b1212624284f4b183|1561622987|1561620583; _pk_id.6.1152=37ba736c7cb6ca79.1561097331.12.1561622989.1561622984."}

    req = urllib.request.Request(url,None,headers)

    u = urllib.request.urlopen(req)

    f = open(file_name, 'wb')
    block_sz = 8192#下载大文件
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        f.write(buffer)
    f.close()
    print ("Sucessful to download" + " " + file_name)


#获取断点续传的循环节点
sql2 = "SELECT * FROM tag"
cursor.execute(sql2)
result = cursor.fetchall()

a = result[0][0]
b = result[0][1]
c = result[0][2]
d = result[0][3]


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
    for i in range(0,len(bigtype['data'])):
        if i <a:
            continue
        print("开始爬取"+bigtype['data'][i]['columnname']+",参数"+bigtype['data'][i]['columnid'])
        field_bigType = str(bigtype['data'][i]['columnname']).strip()
        field_bigTypeCode = str(bigtype['data'][i]['columnid']).strip()
        # 获取一个类型
        curListHtml = parseHtml(getHtml("http://icid.iachina.cn/ICID/front/leafColComType.do?columnid=%s" % field_bigTypeCode,
                             'GBK'))
        print("-------")
        curList = curListHtml.find_all("li",op_id="type_me")
        # 循环获取单条数据
        for j in range(0,len(curList)):
            if i==a and j < b:
                continue
            param = curList[j].find("a").get("id")
            if param != None:
                print(param, curList[j].find("a").get_text())
                type_code = curList[j].get("type_code")
                # 保存数据库字段——公司类型代码
                field_companyTypeCode = str(type_code).strip()
                # 保存数据库字段——公司类型
                field_companyType = str(getComType(type_code)).strip()
                # 保存数据库字段——公司全名代码
                field_companyAllNameCode = str(param).strip()
                # 保存数据库字段——公司全名
                field_companyAllName = str(curList[j].find("a").get_text()).strip()

                #pdf列表页面
                curItemUrl="http://icid.iachina.cn/ICID/front/getCompanyInfos.do?columnid=%s&comCode=%s&attr=01" % (field_bigTypeCode, param)
                curItemList = parseHtml(getHtml(curItemUrl, "GBK")).find("div", class_="jie_nei").find_all("li")
                for x in range(0,len(curItemList)):
                    if i==a and j == b and x < c:
                        continue
                    # 保存数据库字段——信息标题
                    field_informationTitle = curItemList[x].find("a").get_text()
                    # 保存数据库字段——信息标题代码
                    field_informationTitleCode =  curItemList[x].find("a").get("id")
                    # 保存数据库字段——发布时间
                    field_createTime = curItemList[x].find("p", class_="kk").get_text()

                    curItemUrl1 = "http://icid.iachina.cn/ICID/front/infoDetail.do?informationno=%s" % str(
                        field_informationTitleCode)
                    pdfhtml = parseHtml(getHtml(curItemUrl1, "GBK")).find("div", class_="pdf_a").find_all("li")

                    for z in range(0,len(pdfhtml)):
                        if i == a and j == b and x == c and z <= d:
                            continue
                        # 保存数据库字段——信息id
                        field_PDFid = pdfhtml[z].find("a").get("id").strip()

                        pdfurl = "http://icid.iachina.cn/ICID/files/piluxinxi/pdf/" + field_PDFid

                        pdfname = pdfhtml[z].find("a").get_text().strip()
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

                        sql1 = "update tag set a = %d,b = %d,c = %d,d = %d"% (i,j,x,z)
                        cursor.execute(sql1)
                        db.commit()  # 提交事务
                        print(i,j,x,z)

except Exception as e:
    db.rollback()
    raise e # 抛出错误