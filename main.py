#%%
import pika

#%%
connection = pika.BlockingConnection()

channel = connection.channel()
# If exchange does not exist, create it.
channel.exchange_declare(exchange="fever", exchange_type="direct")

# If queue does not exist, create it.
channel.queue_declare(queue="title")

# Bind the queue to the exchange with the given routing key.
channel.queue_bind(queue="title", exchange="fever", routing_key="title")

# Publish to the channel with the given exchange, routing key and body.
for i in range(15):
    channel.basic_publish(exchange="fever", routing_key="title", body=f"Title{i}")


connection.close()


# %%
connection = pika.BlockingConnection()
channel = connection.channel()

while True:
    method_frame, header_frame, body = channel.basic_get("title")
    if method_frame:
        print(method_frame, header_frame, body)
        channel.basic_ack(method_frame.delivery_tag)
    else:
        print("No message returned")
        break

connection.close()
# %%
