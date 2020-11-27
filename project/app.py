import time
from flask import Flask
from flask_cors import *
from pyspark import *


def get_data():
    msg = open("message.txt",'r').readlines()[0]
    while msg == "" or msg == "[]":
        time.sleep(1)
        msg = open("message.txt", 'r').readlines()[0]
    return msg


app = Flask(__name__)
CORS(app, supports_credentials=True)
conf = SparkConf().setMaster("local").setAppName("My App")
sc = SparkContext(conf=conf)

data_list = []
content = []
res = []


@app.route('/getApi', methods=['GET'])
def get():
    global conf
    global sc
    global data_list
    global content
    global res

    data_current = eval(get_data())
    while len(data_list) < 20:
        data_list.append(data_current)
        if not content:
            rdd = sc.parallelize(data_current)
            content = rdd.collect()
        else:
            rdd = sc.parallelize(content)
            rdd_current = sc.parallelize(data_current)
            rdd = rdd.join(rdd_current).map(lambda x: (x[0], x[1][0] + x[1][1]))
            content = rdd.collect()
        data_current = eval(get_data())

    assert content is not []
    data_previous = data_list[0]
    data_list = data_list[1:]
    data_list.append(data_current)
    rdd = sc.parallelize(content)
    rdd_previous = sc.parallelize(data_previous)
    rdd_current = sc.parallelize(data_current)
    rdd = rdd.join(rdd_previous).map(lambda x: (x[0], x[1][0] - x[1][1]))
    rdd = rdd.join(rdd_current).map(lambda x: (x[0], x[1][0] + x[1][1]))
    rdd_res = rdd.map(lambda x: {
        "name": x[0],
        "value": x[1]
    })
    res = str(rdd_res.collect())
    print(res)
    return res


if __name__ == '__main__':
    app.run(port=5050, debug=False)
