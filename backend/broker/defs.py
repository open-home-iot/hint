class HumeMessage:
    """
    Message types for HUME communication, both incoming and outgoing.
    """

    DISCOVER_DEVICES = 0
    ATTACH_DEVICE = 1

    ACTION_STATEFUL = 2
    ACTION_STATES = 5

    UNPAIR = 3
    DETACH = 4

    LATENCY_TEST = 6
