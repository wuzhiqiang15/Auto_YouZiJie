import requests
import readConfig as readConfig
import os
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
from common import configHttp as configHttp
from common.Log import MyLog as Log
import json

localReadConfig = readConfig.ReadConfig()
proDir = readConfig.proDir
localConfigHttp = configHttp.ConfigHttp()
log = Log.get_log()
logger = log.get_logger()

caseNo = 0

# 创建token令牌
def get_visitor_token():
    host = localReadConfig.get_http("BASEURL")
    response = requests.get(host + "/v2/User/Token/generate")
    info = response.json()
    token = info.get("info")
    logger.debug("Create token: %s" % token)
    return token

def set_visitor_token_to_config():
    token_v = get_visitor_token()
    localReadConfig.set_headers("TOKEN_V", token_v)

def get_value_from_return_json(json, name1, name2):
    info = json["info"]
    group = info[name1]
    value = group[name2]
    return value

def show_return_msg(response):
    url = response.url
    msg = response.text
    print("\n请求地址：" + url)
    print("\n请求返回值：" + '\n' + json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))

# ****************************** read testCase excel ********************************
# 从Excel文件中获取接口数据
def get_xls(xls_name, sheet_name):
    cls = []
    # 获取excel文件的路径
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    # 打开excel文件
    file = open_workbook(xlsPath)
    sheet = file.sheet_by_name(sheet_name)
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls

# ****************************** read SQL xml ********************************
database = {}

# 定义一个存放SQL语句的xml
def set_xml():
    if len(database) == 0:
        sql_path = os.path.join(proDir, "testFile", "SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            # print('db_name is: %s',% db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                # print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    # print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table

# 通过指定的name，获取到db的信息
def get_xml_dict(database_name, table_name):
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict

# 通过指定的name和sql_id，获取sql的内容
def get_sql(database_name, table_name, sql_id):
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql

# ****************************** read interfaceURL xml ********************************

def get_url_from_xml(name):
    """
    By name get url from interfaceURL.xml
    :param name: interface's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, "testFile", "interfaceURL.xml")
    tree = ElementTree.parse(url_path)
    for u in tree.findall('url'):
        url_name = u.get('name')
        if url_name == name:
            for c in u.getchildren():
                url_list.append(c.text)

    url = '/v2/' + '/'.join(url_list)
    return url

if __name__ == "__main__":
    print(get_xls("login", "Sheet1"))
    set_visitor_token_to_config()