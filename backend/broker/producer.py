import json

from rabbitmq_client import RMQProducer, QueueParams

from backend.broker.defs import (
    DISCOVER_DEVICES
)


# Producer instance with which to publish messages.
producer: RMQProducer


def init(producer_instance):
    """
    Initialize the producer module.

    :type producer_instance: rabbitmq_client.RMQProducer
    """
    global producer
    producer = producer_instance


def discover_devices(hume_uuid, message_content):
    """
    :type hume_uuid: str
    :param message_content: discover devices message content
    :type message_content: str
    """
    producer.publish(
        json.dumps(
            {
                "type": DISCOVER_DEVICES,
                "content": message_content
            }
        ).encode('utf-8'),
        queue_params=QueueParams(hume_uuid, durable=True)
    )
