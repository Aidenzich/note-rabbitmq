#%%
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
for i in range(150):
    channel.basic_publish(exchange="test", routing_key="test_q", body=f"Title{i}")


connection.close()


# %%
# Get
connection = pika.BlockingConnection()
channel = connection.channel()

while True:
    method_frame, header_frame, body = channel.basic_get("test_q")
    if method_frame:
        print(method_frame, header_frame, body)
        channel.basic_ack(method_frame.delivery_tag)
    else:
        print("No message returned")
        break

connection.close()
# %%
import pika

# Consumer
connection = pika.BlockingConnection()
channel = connection.channel()

for method_frame, properties, body in channel.consume("test_q"):
    # Display the message parts and acknowledge the message
    print(method_frame, properties, body)
    channel.basic_ack(method_frame.delivery_tag)

    # # Escape out of the loop after 10 messages
    # if method_frame.delivery_tag == 10:
    #     break


# Cancel the consumer and return any pending messages
requeued_messages = channel.cancel()
print("Requeued %i messages" % requeued_messages)
connection.close()

# %%
