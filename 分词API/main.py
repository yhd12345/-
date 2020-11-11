from requests import post
import json

from get_hot import get_hot_json_str

if __name__ == '__main__':
    with open("input.json", "w",encoding='utf-8') as f:
        f.write(get_hot_json_str())
    path = 'C:/Users/yhd/Desktop/云计算大作业/分词API/input.json'
    file = open(path, encoding='utf-8')
    contents = file.read()
    search_info = json.loads(contents)
    ret = post('http://localhost:50055/keyWords', json=search_info)
    print(ret.text)