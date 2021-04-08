import sys

if sys.argv[1] == "test":
    from backend.settings.test import *  # noqa
else:
    from backend.settings.local import *  # noqa
