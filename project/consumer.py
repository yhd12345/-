from kafka import KafkaConsumer

if __name__ == '__main__':
    globals()
    consumer = KafkaConsumer('result')
    for msg in consumer:
        message = msg.value.decode('utf-8')
        if message != "[]":
            file = open("message.txt", 'w')
            file.write(message)
            file.close()
        print(message)
