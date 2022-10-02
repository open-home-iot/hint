"""
This module contains shortcut functions to issue standardized commands to a
HUME, such as discover devices, executing device actions, etc.
"""
import datetime
import json

from rabbitmq_client import RMQProducer, QueueParams

from backend.broker.defs import HumeMessage


# Producer instance with which to publish messages.
_producer: RMQProducer


# For testing
class FakeProducer:

    def publish(self, *args, **kwargs):
        ...


def init(producer_instance: RMQProducer):
    """
    Initialize the producer module, sets the module instance to the parameter
    RMQProducer.

    :param producer_instance: RMQProducer instance to set as the global
        instance.
    """
    global _producer
    _producer = producer_instance


def discover_devices(hume_uuid: str, message_content: str):
    """
    Issue a Discover devices command to a HUME.

    :param hume_uuid: UUID of the HUME to send the Discover devices message to.
    :param message_content: discover devices message content.
    """
    global _producer
    _producer.publish(
        json.dumps(
            {
                "type": HumeMessage.DISCOVER_DEVICES,
                "content": message_content
            }
        ).encode('utf-8'),
        queue_params=QueueParams(hume_uuid, durable=True)
    )


def attach(hume_uuid: str, identifier: str):
    """
    Issue an attach command for a device to a HUME.

    :param hume_uuid: UUID of the HUME that discovered the device.
    :param identifier: identifier of the device to attach.
    """
    global _producer
    _producer.publish(
        json.dumps(
            {
                "type": HumeMessage.ATTACH_DEVICE,
                "identifier": identifier
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

        group_id: group ID of a pointed out new device state.
        state_id: new device state.
    """
    payload = {
        "type": HumeMessage.ACTION_STATEFUL,
        "device_uuid": device_uuid,
    }
    payload.update(kwargs)
    global _producer
    _producer.publish(json.dumps(payload).encode('utf-8'),
                      queue_params=QueueParams(hume_uuid, durable=True))


def send_device_action_state_request(hume_uuid: str, device_uuid: str):
    """
    Issue a HUME a request to get all stateful action states for a device.
    """
    payload = {
        "type": HumeMessage.ACTION_STATES,
        "device_uuid": device_uuid
    }
    global _producer
    _producer.publish(json.dumps(payload).encode('utf-8'),
                      queue_params=QueueParams(hume_uuid, durable=True))


def unpair(hume_uuid):
    """
    Issues an unpairing command to the target HUME. This will lead to the HUME
    being factory reset, and any device information is lost on the HUME end.
    """
    payload = {
        "type": HumeMessage.UNPAIR
    }
    global _producer
    _producer.publish(json.dumps(payload).encode('utf-8'),
                      queue_params=QueueParams(hume_uuid, durable=True))


def detach(hume_uuid, device_uuid):
    """
    Issues a detach command to the a hume for a device.
    """
    payload = {
        "type": HumeMessage.DETACH,
        "device_uuid": device_uuid
    }
    global _producer
    _producer.publish(json.dumps(payload).encode('utf-8'),
                      queue_params=QueueParams(hume_uuid, durable=True))


def latency_test(hume_uuid):
    """
    Issue a latency test message to the target HUME.
    """
    payload = {
        "type": HumeMessage.LATENCY_TEST,
        "hint_hume_sent": datetime.datetime.now()
    }
    global _producer
    _producer.publish(json.dumps(payload).encode('utf-8'),
                      queue_params=QueueParams(hume_uuid, durable=True))
