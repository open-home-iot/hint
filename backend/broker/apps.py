import logging
import os
import signal
import functools

import pika

from django.apps import AppConfig
from django.conf import settings

from rabbitmq_client import (
    RMQProducer,
    RMQConsumer,
    ConsumeParams,
    QueueParams
)

from backend.broker.consumer_views import incoming_command
from backend.broker import producer as producer_module


class BrokerConfig(AppConfig):
    name = 'backend.broker'
    has_started = False

    def ready(self):
        """
        Called once the application is ready.

        https://docs.djangoproject.com/en/3.1/ref/applications/
        """
        # Development specific, due to Django code reload ...
        # DEBUG indicates development, RUN_MAIN indicates it's not the
        # reloader reaching this block.
        if settings.DEBUG and not os.environ.get("RUN_MAIN"):
            return

        if BrokerConfig.has_started:
            return
        BrokerConfig.has_started = True

        rmq_client_log_level = logging.INFO

        # Set up queue handler for same process log events
        logger = logging.getLogger("rabbitmq_client")
        logger.setLevel(rmq_client_log_level)

        # Create handler to actually print something
        stream_handler = logging.StreamHandler()
        logger.addHandler(stream_handler)

        formatter = logging.Formatter(fmt="{asctime} {levelname:^8} "
                                      "{name} - {message}",
                                      style="{",
                                      datefmt="%d/%m/%Y %H:%M:%S")
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(rmq_client_log_level)

        credentials = pika.PlainCredentials(settings.HUME_BROKER_USERNAME,
                                            settings.HUME_BROKER_PASSWORD)
        connection_params = pika.ConnectionParameters(
            host=settings.HUME_BROKER_IP,
            port=settings.HUME_BROKER_PORT,
            virtual_host='/',
            credentials=credentials
        )

        hint_master_queue_parameters = QueueParams(
            settings.MASTER_COMMAND_QUEUE_NAME,
            durable=True
        )

        consumer = RMQConsumer(connection_parameters=connection_params)
        consumer.consume(ConsumeParams(incoming_command),
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

        stop_callback = functools.partial(stop_func,
                                          consumer=consumer,
                                          producer=producer)

        signal.signal(signal.SIGINT, stop_callback)
        signal.signal(signal.SIGTERM, stop_callback)
