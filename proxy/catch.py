import json
import os
import signal
import time
import sys

from save import save_api, save_csv, save_case
from format import request_format, response_format

HOST = os.getenv('TEST_HOST')
NAME = os.getenv('TEST_NAME')
port = os.getenv('PROXY_PORT')
filter_headers = ['Postman-Token', 'User-Agent', 'Host', 'accept-encoding', 'Connection', 'cache-control', 'Accept',
                  'content-length', 'Origin', 'Referer']


class Catch(object):

    def __init__(self):
        def handler(signum, frame):
            os.system('networksetup -setwebproxystate "Wi-Fi" off')
            os.system('networksetup -setsecurewebproxystate "Wi-Fi" off')
            sys.exit(0)
        signal.signal(signal.SIGINT, handler)
        os.system('networksetup -setwebproxy "Wi-Fi" 0.0.0.0 ' + str(port))
        os.system('networksetup -setsecurewebproxy "Wi-Fi" 0.0.0.0 ' + str(port))

    @staticmethod
    def response(flow):
        # 保留指定地址的接口请求
        if HOST not in flow.request.pretty_url:
            return
        # 保留返回格式为json的数据
        if 'Content-Type' not in flow.response.headers:
            return
        if 'application/json' not in flow.response.headers['Content-Type']:
            return
        # 保留状态码为200的数据
        if flow.response.status_code != 200:
            return
        body = {}
        variables = []
        request_variables = []
        parameters = []
        request_value = {}
        process = {}

        # 仅保留需要的头信息
        headers = [{'key': k, 'value': v} for k, v in flow.request.headers.items() if k not in filter_headers]
        # 获取api名称
        url = flow.request.pretty_url.split('?')[0].replace(HOST, '')
        name = NAME + '_' + '_'.join(url.split('/')[3:])+'_'+str.lower(flow.request.method)
        # 根据请求方式处理请求参数
        method = flow.request.method
        if flow.request.method == 'GET':
            body = dict(flow.request.query.fields)
        else:
            if flow.request.text:
                body = json.loads(flow.request.text)
        # 处理请求数据
        if body:
            variables, request_variables, parameters, request_value, process = request_format(body)
        # 处理接口返回
        validate = response_format(flow.response.text)

        data = {
            "name": name,
            "variables": variables,
            "request": request_variables,
            "url": url,
            "method": method,
            "headers": headers,
            "parameters": parameters,
            "validate": validate,
            "process": process
        }
        # 保存接口请求数据
        save_csv(name, request_value)
        # 保存api结构
        save_api(name, data)
        # 保存测试流程
        save_case(NAME, data)

addons = [
    Catch()
]
