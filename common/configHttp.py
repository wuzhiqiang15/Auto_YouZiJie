# 定义HTTP请求
import requests
import readConfig as readConfig
from common.Log import MyLog as Log
import json

localReadConfig = readConfig.ReadConfig()

class ConfigHttp(object):
    def __init__(self):
        global scheme, host, port, timeout
        scheme = localReadConfig.get_http("scheme")
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}
        self.state = 0

    def set_url(self, url):
        self.url = scheme + "://" + host + url

    def set_headers(self, header):
        self.headers = header

    def set_params(self, param):
        self.params = param

    def set_data(self, data):
        self.data = data

    def set_files(self, filename):
        if filename != '':
            file_path = "D:/AutoTest_YouZiJie/testFile/img" + filename
            self.files = {'file': open(file_path, 'rb')}
        if filename == '' or filename is None:
            self.state = 1

    # 定义HTTP的GET方法
    def get(self):
        try:
            response = requests.get(self.url, headers=self.headers, params=self.params, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # 定义HTTP的POST方法
    def post(self):
        try:
            response = requests.post(self.url, headers=self.headers, parmas=self.params, data=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out")
            return None

    # 带文件的POST请求
    def postWithFile(self):
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # 带JSON的POST请求
    def postWithJson(self):
        try:
            response = requests.post(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

if __name__ == "__main__":
    print("ConfigHTTP")
