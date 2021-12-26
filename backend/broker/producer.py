"""
This module contains shortcut functions to issue standardized commands to a
HUME, such as discover devices, executing device actions, etc.
"""


import json

from rabbitmq_client import RMQProducer, QueueParams

from backend.broker.defs import MessageType


# Producer instance with which to publish messages.
producer: RMQProducer


def init(producer_instance: RMQProducer):
    """
    Initialize the producer module, sets the module instance to the parameter
    RMQProducer.

    :param producer_instance: RMQProducer instance to set as the global
        instance.
    """
    global producer
    producer = producer_instance


def discover_devices(hume_uuid: str, message_content: str):
    """
    Issue a Discover devices command to a HUME.

    :param hume_uuid: UUID of the HUME to send the Discover devices message to.
    :param message_content: discover devices message content.
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


def attach(hume_uuid: str, device_address: str):
    """
    Issue an attach command for a device to a HUME.

    :param hume_uuid: UUID of the HUME that discovered the device.
    :param device_address: address of the device to attach.
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


def send_device_action(hume_uuid: str,
                       device_uuid: str,
                       **kwargs):
    """
    Issues a device action command to a HUME for a specific device.

    :param hume_uuid: HUME to receive the action.
    :param device_uuid: device to receive the action.

    Possible kwargs:

        For a STATEFUL action, both of these parameters must be provided:

        device_state_group_id: group ID of a pointed out new device state.
        device_state: new device state.
    """
    payload = {
        "type": MessageType.DEVICE_ACTION,
        "device_uuid": device_uuid,
    }
    payload.update(kwargs)
    global producer
    producer.publish(json.dumps(payload).encode('utf-8'),
                     queue_params=QueueParams(hume_uuid, durable=True))


def unpair(hume_uuid):
    """
    Issues an unpairing command to the target HUME. This will lead to the HUME
    being factory reset, and any device information is lost on the HUME end.
    """
    payload = {
        "type": MessageType.UNPAIR
    }
    global producer
    producer.publish(json.dumps(payload).encode('utf-8'),
                     queue_params=QueueParams(hume_uuid, durable=True))

