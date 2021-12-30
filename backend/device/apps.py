from django.apps import AppConfig


class DeviceConfig(AppConfig):
    name = 'backend.device'

    def ready(self):
        import backend.device.signal_handlers  # noqa
