from django.apps import AppConfig


class HumeConfig(AppConfig):
    name = 'hume'

    def ready(self):
        # Used to register signals for this application, in this case post_delete for users.
        # NOTE! This will not work on its own, you need to define default_app_config in __init__.py for the application
        # you want to register a signal for.
        import hume.signals
