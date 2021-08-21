import json

from rabbitmq_client import RMQProducer, QueueParams

from backend.broker.defs import MessageType


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
    global producer
    producer.publish(
        json.dumps(
            {
                "type": MessageType.DISCOVER_DEVICES,
                "content": message_content
            }
        ).encode('utf-8'),
        queue_params=QueueParams(hume_uuid, durable=True)
    )


def attach(hume_uuid, device_address):
    """
    :param hume_uuid: UUID of the HUME that discovered the device
    :param device_address: address of the device to attach
    """
    global producer
    producer.publish(
        json.dumps(
            {
                "type": MessageType.ATTACH_DEVICE,
                "device_address": device_address
            }
        ).encode('utf-8'),
        queue_params=QueueParams(hume_uuid, durable=True)
    )


def send_device_action(hume_uuid,
                       device_uuid,
                       **kwargs):
    """
    :param hume_uuid: HUME to receive the action
    :param device_uuid: device to receive the action

    Possible kwargs:

        device_state_group_id: group ID of a pointed out new device state
        device_state: new device state
    """
    payload = {
        "type": MessageType.DEVICE_ACTION,
        "device_uuid": device_uuid,
    }
    payload.update(kwargs)
    global producer
    producer.publish(json.dumps(payload).encode('utf-8'),
                     queue_params=QueueParams(hume_uuid, durable=True))
