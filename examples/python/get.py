import pika

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
