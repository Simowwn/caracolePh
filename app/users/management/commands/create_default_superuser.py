from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser if none exists"

    def handle(self, *args, **options):
        existing_superuser = User.objects.filter(
            email=settings.SUPERUSER_EMAIL,
        ).exists()

        if not existing_superuser:
            User.objects.create_superuser(
                email=settings.SUPERUSER_EMAIL,
                password=settings.SUPERUSER_PASSWORD,
                first_name="Webdev",
                last_name="Dexterton",
                is_staff=True,
                is_superuser=True,
                is_active=True,
            )
            self.stdout.write(self.style.SUCCESS("Superuser created."))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser already exists."))
