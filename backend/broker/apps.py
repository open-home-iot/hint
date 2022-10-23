import logging
import os
import signal
import functools
import json
import sys
import time

import pika

from typing import Callable

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.apps import AppConfig
from django.conf import settings

from rabbitmq_client import (
    RMQProducer,
    RMQConsumer,
    ConsumeParams,
    QueueParams,
    ConsumeOK
)

from backend.broker import producer as producer_module
from backend.broker import HumeMessage


LOGGER = logging.getLogger(__name__)


def incoming_message(message: bytes, ack: Callable = None, **kwargs):
    """
    ! NOTE ! Avoid putting expensive operations here or this will become a
    bottleneck and a half. No database lookups allowed!
    """
    if isinstance(message, ConsumeOK):
        return

    decoded_event = json.loads(message.decode('utf-8'))

    hume_event = {
        # Setting the "type" field here will lead to hume_event being
        # invoked for consumers listening on the HUME's UUID group/topic.
        "type": "hume.event",
        "uuid": decoded_event["uuid"],
        "event_type": decoded_event["type"],
        "content": decoded_event["content"]
    }

    if decoded_event.get("device_uuid") is not None:
        hume_event["device_uuid"] = decoded_event["device_uuid"]

    if decoded_event["type"] == HumeMessage.LATENCY_TEST:
        hume_event["content"]["hint_hume_returned"] = time.time_ns()

    # Dispatch message to websocket consumers.
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(decoded_event["uuid"],
                                            hume_event)

    ack()


class BrokerConfig(AppConfig):
    name = 'backend.broker'

    def ready(self):
        """
        Called once the application is ready.

        https://docs.djangoproject.com/en/3.1/ref/applications/
        """
        # Development specific, due to Django code reload ...
        # DEV_MODE indicates we're using runserver (it's set when you run
        # commands via manage.py).
        # RUN_MAIN indicates it's not the reloader reaching this block.
        if (bool(os.environ.get("DEV_MODE")) and
                not bool(os.environ.get("RUN_MAIN"))):
            LOGGER.info("DEV_MODE environment variable is set, requiring the "
                        "'RUN_MAIN' variable to also be set in order to start"
                        "RabbitMQ connections.")
            return

        credentials = pika.PlainCredentials(settings.HUME_BROKER_USERNAME,
                                            settings.HUME_BROKER_PASSWORD)
        connection_params = pika.ConnectionParameters(
            host=settings.HUME_BROKER_HOST,
            port=settings.HUME_BROKER_PORT,
            virtual_host=settings.HUME_BROKER_VHOST,
            credentials=credentials
        )

        hint_master_queue_parameters = QueueParams(
            settings.MASTER_COMMAND_QUEUE_NAME,
            durable=True
        )

        consumer = RMQConsumer(connection_parameters=connection_params)
        consumer.consume(ConsumeParams(incoming_message),
                         queue_params=hint_master_queue_parameters)

        producer = RMQProducer(connection_parameters=connection_params)
        producer_module.init(producer)

        consumer.start()
        producer.start()

        def stop_func(_s,
                      _f,
                      consumer=None,
                      producer=None):
            """
            :param _s: signal leading to stop
            :param _f: frame when stop was called
            :param consumer: rabbitmq_client.RMQConsumer
            :param producer: rabbitmq_client.RMQProducer
            """
            consumer.stop()
            producer.stop()
            sys.exit()

        stop_callback = functools.partial(stop_func,
                                          consumer=consumer,
                                          producer=producer)

        signal.signal(signal.SIGINT, stop_callback)
        signal.signal(signal.SIGTERM, stop_callback)
