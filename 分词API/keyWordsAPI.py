import json
from flask import Flask, jsonify, request, abort
# 从textrank4zh模块中导入提取关键词和生成摘要的类
from textrank4zh import TextRank4Keyword, TextRank4Sentence


def keyword(data,content):
    # 创建分词类的实例
    tr4w = TextRank4Keyword()
    # 对文本进行分析，设定窗口大小为2，并将英文单词小写
    tr4w.analyze(text=content, lower=True, window=2)
    l = []
    # 从关键词列表中获取前5个关键词
    for item in tr4w.get_keywords(num=5, word_min_len=1):
        # 打印每个关键词的内容及关键词的权重
        l.append(item.word)
    data['keyWords'] = l
    return


app = Flask(__name__)


@app.route('/keyWords', methods=['POST'])
def getKeyWords():
    if not request.json:
        abort(400)
    search_info = request.json
    res=[]
    for info in search_info:
        data = {'id': info['id'], 'keyWords': '', 'metrics': info['metrics']}
        if data['metrics']!='盐选会员':
            s=data['metrics'].split(' ')
            data['metrics']=int(s[0])
        title = info['title']
        keyword(data, title)
        res.append(data)
    json_str = json.dumps(res, ensure_ascii=False, indent=4)
    with open("output.json", "w") as f:
        f.write(json_str)
    return json_str


if __name__ == '__main__':
    app.run(port=50055, debug=True)
