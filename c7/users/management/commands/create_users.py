from django.core.management import BaseCommand

from users.models import User

values = ['admin', 'staff', 'user1', 'user2', 'user3']
domain = 'test.com'


class Command(BaseCommand):

    def handle(self, *args, **options):
        for value in values:
            if not User.objects.filter(email=value + '@' + domain).exists():
                user = User.objects.create(
                    email=value + '@' + domain,
                    first_name=value.title(),
                    last_name=value.title(),
                    is_superuser=True if value == 'admin' else False,
                    is_staff=True if (
                            value == 'admin' or value == 'staff') else False,
                    is_active=True,
                )
                user.set_password('12345')
                user.save()
            else:
                continue
