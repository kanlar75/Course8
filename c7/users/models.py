from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

NULLABLE = {'blank': True, 'null': True}


class UserManager(BaseUserManager):
    """ Собственный класс Manager """

    def create_user(self, email, password=None):
        """ Создает и возвращает пользователя с email, паролем """

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """ Создает и возвращает пользователя с привилегиями superuser """

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=250, unique=True,
                              verbose_name='Адрес электронной почты')
    first_name = models.CharField(max_length=100, **NULLABLE,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=100, **NULLABLE,
                                 verbose_name='Фамилия')
    avatar = models.ImageField(upload_to='users/', **NULLABLE,
                               verbose_name='Аватар')
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')
    chat_id = models.CharField(max_length=20, unique=True, **NULLABLE,
                               verbose_name='id_chat в Telegram')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
