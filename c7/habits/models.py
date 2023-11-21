from django.db import models

from config import settings
from users.models import NULLABLE


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='создатель привычки',
                             **NULLABLE)
    place = models.CharField(max_length=50, verbose_name='место выполнения '
                                                         'привычки')
    time = models.TimeField(verbose_name='время выполнения привычки')
    action = models.CharField(max_length=150, verbose_name='действие')
    is_pleasant = models.BooleanField(default=False,
                                      verbose_name='приятная привычка')
    connected_habit = models.ForeignKey('self',
                                        on_delete=models.SET_NULL,
                                        verbose_name='связанная привычка',
                                        **NULLABLE)
    periodicity = models.SmallIntegerField(default=1,
                                           verbose_name='периодичность')
    reward = models.CharField(max_length=150, verbose_name='награда',
                              **NULLABLE)
    estimated_time = models.SmallIntegerField(default=120,
                                              verbose_name='время на '
                                                           'выполнение')
    is_public = models.BooleanField(default=False,
                                    verbose_name='публичная привычка')
    last_reminder = models.DateTimeField(verbose_name='Последнее напоминание',
                                         **NULLABLE)

    def __str__(self):
        return f'{self.action} в {self.time}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ('id',)
