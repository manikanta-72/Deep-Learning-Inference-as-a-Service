import pika
import requests
import time
import numpy as np

time.sleep(20)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='10.123.129.36'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')
    
def on_request(ch, method, props, body):
    data = body

    SERVER_URL = 'http://new-resnet-cluster-ip-service:8501/v1/models/resnet_classification:predict'
    
    response = requests.post(SERVER_URL, data= data)

    prediction = response.json()['predictions'][0]

    answer = np.argmax(prediction)
    print("receiver response:", response.json())
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(answer)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
