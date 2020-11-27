import jieba.analyse
from bs4 import BeautifulSoup
import json
import requests

url = 'https://www.zhihu.com/billboard'
headers = {"User-Agent": "", "Cookie": ""}


def wrap(error_code, content):
    return {
        'error_code': error_code,
        'content': content
    }


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


def key_word(data, content):
    l = jieba.analyse.extract_tags(content, topK=5, allowPOS=('n', 'nr', 'ns', 'nt', 'nz'))
    data['keyWords'] = l


def get_keywords() -> []:
    search_info = get_hot_json()
    res = []
    for info in search_info:
        data = {'id': info['id'], 'keyWords': '', 'metrics': info['metrics']}
        if '盐选' not in data['metrics']:
            s = data['metrics'].split(' ')
            data['metrics'] = int(s[0])
        else:
            data['metrics'] = 500
        title = info['title']
        key_word(data, title)
        res.append(data)
    return res


def format_res(res: []) -> str:
    result = "init 0"
    for group in res:
        for keyword in group['keyWords']:
            result += '\n'
            result += keyword
            result += " "
            result += str(group['metrics'])
    return result


if __name__ == '__main__':
    print(format_res(get_keywords()))
