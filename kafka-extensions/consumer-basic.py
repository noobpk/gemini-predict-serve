from kafka import KafkaConsumer

consumer = KafkaConsumer('gemini-data-streaming',
                        bootstrap_servers=['localhost:9092'],
                        auto_offset_reset='earliest', 
                        enable_auto_commit=False)

for message in consumer:
    print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                          message.offset, message.key,
                                          message.value))