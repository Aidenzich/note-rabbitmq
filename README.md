# RabbitMQ with Python
RabbitMQ is a popular open source message broker that implements the Advanced Message Queuing Protocol (AMQP). It allows you to easily exchange messages between applications, services, and servers in a flexible and reliable way.

In this repository, you will find a guide on how to work with RabbitMQ using Python. The guide covers the basics of RabbitMQ and how to use it with Python, including how to install and set it up, how to send and receive messages, and how to use exchanges and queues.

If you are new to RabbitMQ, this repo should provide you with the knowledge and tools you need to start using RabbitMQ with Python in your own projects.

## RabbitMQ exchange structure
![](docs/imgs/exchanges-topic-fanout-direct.png)
### Roles in RabbitMQ
| Role | Description |
|-|-|
| Producer | Producers are those client applications that publish (write) messages to RabbitMQ |
| Consumer | Consumers are those that subscribe to (read and process) these messages. |
| Queue    | A collection of entities that are maintained in a sequence and can be modified by the addition of entities at one end of the sequence and the removal of entities from the other end of the sequence.  |
| Exchange |  Exchange is used as a routing mediator, to receive messages from producers and push them to message queues according to rules provided by the RabbitMQ exchange type.   |
| Message  | A message can include any kind of information. |