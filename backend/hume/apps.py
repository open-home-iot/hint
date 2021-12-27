from django.apps import AppConfig


class HumeConfig(AppConfig):

    name = 'backend.hume'

    def ready(self):
        import backend.hume.signal_handlers  # noqa
