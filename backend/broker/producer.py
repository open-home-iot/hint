from rabbitmq_client.client import RMQClient


class Producer:
    client: RMQClient

    @classmethod
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
