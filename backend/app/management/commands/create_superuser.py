from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    """
    Django management command to create a superuser account in production environment using environment variables.
    """
    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            try:
                username = settings.SUPER_USER
                email = settings.SUPER_EMAIL
                password = settings.SUPER_PASS

                if not all([username, email, password]):
                    self.stdout.write('Environment variables for superuser not set properly')
                    return

                User.objects.create_superuser(username, email, password)
                self.stdout.write('Superuser created successfully')
            except Exception as e:
                self.stdout.write(f'Failed to create superuser: {str(e)}')
        else:
            self.stdout.write('Superuser already exists')
