import csv
import pystache
import yaml
import json
import os

from pathlib import Path
from functools import reduce


is_update = False
is_new = False
is_need_tab = False
is_suit = False


def save_case(name, data):
    name += '_process'
    cache_name = data['name']
    path_suit = "./testsuites/" + name + "_testsuits.yml"
    suit_file = Path(path_suit)
    if not suit_file.is_file():
        data['name'] = name
        suit = open("./template/test_process_suit.mustache", "r")
        suit_content = pystache.render(suit.read(), data)
        with open(path_suit, 'w') as f:
            f.writelines(suit_content)
    path_case = "./testcases/" + name + "_testcase.yml"
    case_file = Path(path_case)
    data['name'] = cache_name
    if case_file.is_file():
        with open(path_case, 'r') as f:
            testcases = yaml.load(f.read())
        if data['variables']:
            case = open("./template/process_case.mustache", "r")
        else:
            case = open("./template/process_case_null.mustache", "r")
        case_content = pystache.render(case.read(), data)
        testcases['teststeps'].append(yaml.load(case_content))
        testcases = yaml.dump(testcases, allow_unicode=True)
    else:
        case = open("./template/process.mustache", "r")
        testcases = pystache.render(case.read(), data)

    with open(path_case, 'w') as f:
        f.writelines(testcases)



def save_api(name, data):

    global is_need_tab
    global is_suit

    is_need_tab = False

    # 如果suit文件已存在则直接新增testcases，不存在则新增suit文件
    test_name = os.getenv('TEST_NAME')
    path_suit = "./testsuites/" + test_name + "_single_api_testsuits.yml"
    suit = Path(path_suit)
    is_suit = suit.is_file()

    # 判断使用的模版
    if data['variables']:
        if data['method'] == 'GET':
            api = open("./template/params_api.mustache", "r")
        else:
            is_need_tab = True
            api = open("./template/json_api.mustache", "r")
        case = open("./template/test_case.mustache", "r")
        if is_suit:
            suit = open("./template/test_suit_case.mustache", "r")
        else:
            suit = open("./template/test_suit.mustache", "r")
    else:
        api = open("./template/null_api.mustache", "r")
        case = open("./template/test_case_null.mustache", "r")
        if is_suit:
            suit = open("./template/test_suit_case_null.mustache", "r")
        else:
            suit = open("./template/test_suit_null.mustache", "r")

    # 如果api文件存在,且需要新增,则覆盖之前的yaml文件
    path = "../data/" + name + "_api.csv"
    path_api = Path(path)
    if path_api.is_file() and is_update:
        # 从csv文件中获取新的请求结构
        with open(path, 'r') as f:
            header = list(csv.reader(f))[0]
        case2 = ''
        case1 = ''
        dic = {}
        for i in header:
            if '_' in i:
                list1 = i.split('_')
                num = len(list1)-1
                str1 = '{"' + '":{"'.join(list1) + '": "$' + i + '"}' + '}' * num
                str1 = json.loads(str1)
                dic = mix(str1, dic)
            else:
                case1 += '        ' + i + ': $' + i + '\n'
            case2 += '\n    ' + i + ': $' + i
        if is_need_tab:
            case1 += '        ' + yaml.dump(dic).replace('\n', '\n        ')

        case1 = '\n' + case1

        data['variables'] = case2[5:]
        data['request'] = case1[9:]

        update_api(name, data, api, case, suit)
    elif is_new:
        update_api(name, data, api, case, suit)


def save_csv(name, request):
    global is_update
    global is_new

    path = '../data/' + name
    csv_file = Path('../data/' + name + '_api.csv')
    # 如果csv文件已存在则直接新增数据，不存在则新增csv文件

    if csv_file.is_file():
        with open(path + '_api.csv', 'r') as f:
            data = list(csv.reader(f))
            keys = list(request.keys())
            keys = set(keys)
            data_key = set(data[0])
            # 判断本次请求的参数种类和之前保存的是否一致，一致则直接新增，不一致则进行处理
            if keys - data_key:
                # 获取当前请求和csv数据的对称差集
                diff = keys ^ data_key
                # 获取当前csv数据中不存在的参数名
                diff = list(diff - data_key)
                if len(diff) > 0:
                    data[0] += diff
                values = []
                # 为当前请求补充上csv存在，但是本次请求中没有的数据
                for i in data[0]:
                    if i not in request:
                        values.append('')
                    else:
                        values.append(request[i])
                # 检查当前请求数据是否已存在
                if values not in data:
                    data.append(values)
                # 若本次请求有新增参数，则为之前没有该参数的数据补上数据
                for i in range(1, len(data)):
                    num = len(data[0]) - len(data[i])
                    if num != 0:
                        col_add = [''] * num
                        data[i] += col_add
                is_update = True
                is_new = False
            else:
                is_new = False
                is_update = False
                values = list(request.values())
                if values not in data:
                    data.append(values)
        with open(path + '_api.csv', 'w') as f:
            writer = csv.writer(f)
            for i in data:
                writer.writerows([i])
    else:
        is_update = False
        is_new = True

        if request:
            with open(path + '_api.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerows([list(request.keys())])
                writer.writerows([list(request.values())])



def mix(dica, dicb):
    dic = {}
    for key in dica:
        if dicb.get(key):
            if dica[key] != dicb[key]:
                dic[key] = [dica[key], dicb[key]]

                dic[key] = reduce(mix, dic[key])
            else:
                dic[key] = dica[key]
        else:
            dic[key] = dica[key]

    for key in dicb:
        if dica.get(key):
            pass
        else:
            dic[key] = dicb[key]

    return dic


def update_api(name, data, api, case, suit):
    # 开始组合数据
    if is_need_tab:
        # 调整数据写到yaml文件的缩进
        data['variables'] = data['variables'].replace('\n    ', '\n    ')
    api_content = pystache.render(api.read(), data)
    if '\n' in data['variables']:
        data['variables'] = data['variables'].replace('\n    ', '\n        ')
    case_content = pystache.render(case.read(), data)

    suit_content = pystache.render(suit.read(), data)

    # 开始写入数据
    path_api = "../api/" + name + "_api.yml"
    path_case = "./testcases/singleinterface/" + name + "_testcase.yml"
    test_name = os.getenv('TEST_NAME')
    path_suit = "./testsuites/" + test_name + "_single_api_testsuits.yml"

    if is_suit:
        with open(path_suit, 'r') as f:
            testsuits = yaml.load(f.read())
        testsuits['testcases'] = dict(testsuits['testcases'], **yaml.load(suit_content))
        testsuits = yaml.dump(testsuits).replace('\n    ', '\n      ').replace('\n  ', '\n    ')
    else:
        testsuits = suit_content

    with open(path_api, 'w') as f:
        f.writelines(api_content)
    with open(path_case, 'w') as f:
        f.writelines(case_content)
    with open(path_suit, 'w') as f:
        f.writelines(testsuits)
