from django.apps import AppConfig


class HumeConfig(AppConfig):
    name = 'backend.hume'

    def ready(self):
        # Used to register signals for this application, in this case post_delete for users.
        print("READYREADY")
        import backend.hume.signals  # noqa
