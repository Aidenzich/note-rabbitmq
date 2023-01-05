import pika

# Producer
connection = pika.BlockingConnection()

channel = connection.channel()
# If exchange does not exist, create it.
channel.exchange_declare(exchange="test", exchange_type="direct")

# If queue does not exist, create it.
channel.queue_declare(queue="test_q")

# Bind the queue to the exchange with the given routing key.
channel.queue_bind(queue="test_q", exchange="test", routing_key="test_q")

# Publish to the channel with the given exchange, routing key and body.
for i in range(1000000):
    channel.basic_publish(exchange="test", routing_key="test_q", body=f"Title{i}")


connection.close()
