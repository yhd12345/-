from kafka import KafkaProducer
from pyspark import SparkContext
from pyspark.streaming import StreamingContext


def get_list(rdd_list):
    res = []
    for elm in rdd_list:
        tmp = (elm[0], elm[1])
        res.append(tmp)
    return str(res)


def sendmsg(rdd):
    if rdd.count != 0:
        msg = get_list(rdd.collect())
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        producer.send("result", msg.encode('utf8'))
        producer.flush()


if __name__ == '__main__':
    sc = SparkContext("local[2]", "NetworkWordCount")
    sc.setLogLevel("ERROR")
    ssc = StreamingContext(sc, 1)
    lines = ssc.socketTextStream("localhost", 9999)
    words = lines.map(lambda line: (line.split(" ")[0], int(line.split(" ")[1])))
    wordCounts = words.reduceByKey(lambda x, y: x + y)
    wordCounts.foreachRDD(lambda rdd: sendmsg(rdd))
    wordCounts.count()
    ssc.start()
    ssc.awaitTermination()
