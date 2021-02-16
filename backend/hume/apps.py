from django.apps import AppConfig


class HumeConfig(AppConfig):
    # pylint: disable=missing-class-docstring
    name = 'backend.hume'

#    def ready(self):
        # Used to register signals for this application, in this case post_delete for users.
#        import backend.hume.signals  # noqa
