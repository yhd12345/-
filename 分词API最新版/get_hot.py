from bs4 import BeautifulSoup
import json
import requests


def wrap(error_code, content):
    return {
        'error_code': error_code,
        'content': content
    }


url = 'https://www.zhihu.com/billboard'
headers = {"User-Agent": "", "Cookie": ""}


def get_hot_zhihu():
    res = requests.get(url, headers=headers)
    content = BeautifulSoup(res.text, "html.parser")
    hot_data = content.find('script', id='js-initialData').string
    hot_json = json.loads(hot_data)
    hot_list = hot_json['initialState']['topstory']['hotList']
    return hot_list


def get_hot_json():
    res = []
    dict_hot = get_hot_zhihu()
    # dict_hot = []
    idx = 0
    for item in dict_hot:
        idx += 1
        dic = {
            'id': idx,
            'title': '',
            'content': '',
            'metrics': ''
        }

        target = item['target']
        dic['title'] = target['titleArea']['text']
        dic['content'] = target['excerptArea']['text']
        dic['metrics'] = target['metricsArea']['text']

        res.append(dic)

    return res

