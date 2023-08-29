from kafka import KafkaProducer
import json
from time import sleep
from datetime import datetime
import random 
import ipaddress

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
for e in range(100):
    now = datetime.now()
    key = b'time_series'
    accuracy_value = random.uniform(0.0, 100.0)

    # Generate a random IPv4 or IPv6 address
    is_ipv4 = random.choice([True, False])
    if is_ipv4:
        ip = ipaddress.IPv4Address(random.randint(0, 2**32 - 1))
    else:
        ip = ipaddress.IPv6Address(random.randint(0, 2**128 - 1))

    payload = {'time': now.strftime('%Y-%m-%d %H:%M:%S'), 'ip': str(ip), 'score': accuracy_value}
    producer.send('gemini-data-streaming', key=key, value=payload)
    print(payload)
    sleep(1)