import sys

if sys.argv[1] == "test":
    from backend.settings.test import *
else:
    from backend.settings.local import *  # noqa
