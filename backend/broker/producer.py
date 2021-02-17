import json

from rabbitmq_client.client import RMQClient


DISCOVER_DEVICES = 0


class Producer:
    """Static class to host client producing utilities"""
    # pylint: disable=too-few-public-methods

    client: RMQClient

    @staticmethod
    def command(hume_uuid, message):
        """
        :type hume_uuid: str
        :type message: bytes
        """
        Producer.client.command(hume_uuid, message)


def init(client):
    """
    Initialize the producer module.

    :type client: RMQClient
    """
    Producer.client = client


def discover_devices(hume_uuid, message_content):
    """
    :param message_content: discover devices message content
    :type message_content: str
    """
    Producer.command(
        hume_uuid,
        json.dumps(
            {
                "type": DISCOVER_DEVICES,
                "content": message_content
            }
        ).encode('utf-8')
    )
