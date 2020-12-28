"""
This module defines handling for incoming hub (HUME) events.
"""


def incoming_command_queue_message(message):
    """
    :param message: message from the HINT master command queue
    :type message: bytes
    """
    print(message)
