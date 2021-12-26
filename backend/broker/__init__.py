import sys

from .defs import MessageType  # noqa

if len(sys.argv) > 1 and sys.argv[1] == "test":
    from backend.broker import producer
    producer._producer = producer.FakeProducer()
