import pika
import logging
import os
import signal
import functools

from logging.handlers import QueueHandler, QueueListener
from multiprocessing import Queue

from django.apps import AppConfig
from django.conf import settings

from rabbitmq_client.client import RMQClient

from backend.broker.consumer_views import incoming_command_queue_message
from backend.broker import producer


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
        RUN_MAIN = os.environ.get("RUN_MAIN")
        print(f"settings.DEBUG: {settings.DEBUG}")
        print(f"RUN_MAIN: {RUN_MAIN}")
        if settings.DEBUG and not RUN_MAIN:
            return

        print(f"BrokerConfig.has_started: {BrokerConfig.has_started}")
        if BrokerConfig.has_started:
            return
        BrokerConfig.has_started = True

        RMQ_CLIENT_LOG_LEVEL = logging.INFO

        # Set up queue handler for same process log events
        logger = logging.getLogger("rabbitmq_client")
        logger.setLevel(RMQ_CLIENT_LOG_LEVEL)

        log_queue = Queue()
        handler = QueueHandler(log_queue)
        handler.setLevel(RMQ_CLIENT_LOG_LEVEL)
        logger.addHandler(handler)

        # Create handler to actually print something
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt="{asctime} {levelname:^8} "
                                      "{name} - {message}",
                                      style="{",
                                      datefmt="%d/%m/%Y %H:%M:%S")
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(RMQ_CLIENT_LOG_LEVEL)

        # Start queue monitor
        listener = QueueListener(
            log_queue,
            stream_handler,
            respect_handler_level=True
        )
        listener.start()

        credentials = pika.PlainCredentials(settings.HUME_BROKER_USERNAME,
                                            settings.HUME_BROKER_PASSWORD)
        connection_params = pika.ConnectionParameters(
            host=settings.HUME_BROKER_IP,
            port=settings.HUME_BROKER_PORT,
            virtual_host='/',
            credentials=credentials
        )

        client = RMQClient(log_queue=log_queue,
                           connection_parameters=connection_params,
                           daemonize=True)
        client.start()
        client.command_queue(settings.MASTER_COMMAND_QUEUE_NAME,
                             incoming_command_queue_message)
        producer.init(client)

        def stop_func(signal,
                      frame,
                      client=None,
                      queue_listener=None,
                      log_queue=None):
            """Stop client"""
            client.stop()
            queue_listener.stop()
            log_queue.close()

        stop_callback = functools.partial(stop_func,
                                          client=client,
                                          queue_listener=listener,
                                          log_queue=log_queue)

        signal.signal(signal.SIGINT, stop_callback)
        signal.signal(signal.SIGTERM, stop_callback)
