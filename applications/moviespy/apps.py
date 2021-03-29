from django.apps import AppConfig


class MoviespyConfig(AppConfig):
    name = 'applications.moviespy'

    def ready(self):
        from . import updater
        updater.start()
        updater.drive()
