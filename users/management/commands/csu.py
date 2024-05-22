import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from config.settings import PATH_DB
from users.models import User

load_dotenv(PATH_DB)


class Command(BaseCommand):

    def handle(self, *args, **options):
       user = User.objects.create(
            email=os.getenv('ADMIN_EMAIL'),
            first_name='Admin',
            last_name='Ilya',
            is_staff=True,
            is_superuser=True
        )

       user.set_password(os.getenv('PASSWORD_DB'))
       user.save()
