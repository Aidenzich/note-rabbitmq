#%%
import functools
import logging
import pika
import threading
import time

LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


def ack_message(channel, delivery_tag):
    """Note that `channel` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        pass


def do_work(connection, channel, delivery_tag, body):
    thread_id = threading.get_ident()
    # fmt1 = "Thread id: {} Delivery tag: {} Message body: {}"
    # LOGGER.info(fmt1.format(thread_id, delivery_tag, body))
    # Sleeping to simulate 10 seconds of work
    time.sleep(5)
    print(body.decode("utf-8"))
    cb = functools.partial(ack_message, channel, delivery_tag)
    connection.add_callback_threadsafe(cb)


def on_message(channel, method_frame, header_frame, body, args):
    (connection, threads) = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(connection, channel, delivery_tag, body))
    t.start()
    threads.append(t)


credentials = pika.PlainCredentials("guest", "guest")
# Note: sending a short heartbeat to prove that heartbeats are still
# sent even though the worker simulates long-running work
parameters = pika.ConnectionParameters(
    "localhost", credentials=credentials, heartbeat=5
)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.exchange_declare(
    exchange="test",
    exchange_type="direct",
)
channel.queue_declare(queue="test_q")
channel.queue_bind(queue="test_q", exchange="test", routing_key="test_q")

# Note: prefetch is set to 1 here as an example only and to keep the number of threads created
# to a reasonable amount. In production you will want to test with different prefetch values
# to find which one provides the best performance and usability for your solution
channel.basic_qos(prefetch_count=5)

threads = []
on_message_callback = functools.partial(on_message, args=(connection, threads))
channel.basic_consume(on_message_callback=on_message_callback, queue="test_q")

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

# Wait for all to complete
for thread in threads:
    thread.join()

connection.close()

# %%
