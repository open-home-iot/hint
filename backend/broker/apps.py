import logging
import os
import signal
import functools

from logging.handlers import QueueHandler, QueueListener
from multiprocessing import Queue

import pika

from django.apps import AppConfig
from django.conf import settings

from rabbitmq_client.client import RMQClient

from backend.broker.consumer_views import incoming_command
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
        run_main = os.environ.get("RUN_MAIN")
        print(f"settings.DEBUG: {settings.DEBUG}")
        print(f"RUN_MAIN: {run_main}")
        if settings.DEBUG and not run_main:
            return

        print(f"BrokerConfig.has_started: {BrokerConfig.has_started}")
        if BrokerConfig.has_started:
            return
        BrokerConfig.has_started = True

        rmq_client_log_level = logging.INFO

        # Set up queue handler for same process log events
        logger = logging.getLogger("rabbitmq_client")
        logger.setLevel(rmq_client_log_level)

        log_queue = Queue()
        handler = QueueHandler(log_queue)
        handler.setLevel(rmq_client_log_level)
        logger.addHandler(handler)

        # Create handler to actually print something
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt="{asctime} {levelname:^8} "
                                      "{name} - {message}",
                                      style="{",
                                      datefmt="%d/%m/%Y %H:%M:%S")
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(rmq_client_log_level)

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
                             incoming_command)
        producer.init(client)

        def stop_func(_s,
                      _f,
                      rmq_client=None,
                      client_log_queue=None,
                      log_queue_listener=None):
            """
            :param _s: signal leading to stop
            :param _f: frame when stop was called
            :param rmq_client: RMQClient
            :param client_log_queue: Log queue
            :param log_queue_listener: Log queue listener
            """
            rmq_client.stop()
            log_queue_listener.stop()
            client_log_queue.close()

        stop_callback = functools.partial(stop_func,
                                          rmq_client=client,
                                          client_log_queue=log_queue,
                                          log_queue_listener=listener)

        signal.signal(signal.SIGINT, stop_callback)
        signal.signal(signal.SIGTERM, stop_callback)
