import sys

from .defs import HumeMessage  # noqa

if len(sys.argv) > 1 and sys.argv[1] == "test":
    from backend.broker import producer
    producer._producer = producer.FakeProducer()
