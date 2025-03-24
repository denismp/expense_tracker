from django.core.management.commands.runserver import Command as RunserverCommand


class Command(RunserverCommand):
    def handle(self, *args, **options):
        options['use_reloader'] = False
        super().handle(*args, **options)
