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
                           connection_parameters=connection_params)
        client.start()
        # client.command_queue(settings.MASTER_COMMAND_QUEUE_NAME,
        #                      )

        def stop(signum, frame, client=None, listener=None, log_queue=None):
            """Stops the RMQ client on interrupt"""
            print("Stopping client...")
            client.stop()
            print("Stopping queue listener...")
            listener.stop()
            print("Stopping log queue")
            log_queue.close()

        callback = functools.partial(
            stop,
            client=client,
            listener=listener,
            log_queue=log_queue
        )

        signal.signal(signal.SIGINT, callback)
