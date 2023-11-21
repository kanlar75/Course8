from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@test.com',
            first_name='Admin',
            last_name='Admin',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password('12345')
        user.save()

        user = User.objects.create(
            email='user1@test.com',
            first_name='User1',
            last_name='User1',
            is_superuser=False,
            is_staff=False,
            is_active=True
        )
        user.set_password('12345')
        user.save()

        user = User.objects.create(
            email='user2@test.com',
            first_name='User2',
            last_name='User2',
            is_superuser=False,
            is_staff=False,
            is_active=True
        )
        user.set_password('12345')
        user.save()

        user = User.objects.create(
            email='user3@test.com',
            first_name='User3',
            last_name='User3',
            is_superuser=False,
            is_staff=False,
            is_active=True
        )
        user.set_password('12345')
        user.save()

        user = User.objects.create(
            email='staff@test.com',
            first_name='Staff',
            last_name='Staff',
            is_superuser=False,
            is_staff=True,
            is_active=True,

        )
        user.set_password('12345')
        user.save()
