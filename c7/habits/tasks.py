from telebot import TeleBot
from celery import shared_task

from config.settings import TELEGRAM_TOKEN
from habits.servises import get_habits
from django.utils import timezone
bot = TeleBot(TELEGRAM_TOKEN)


@shared_task(name='send_message')
def send_habit_message():
    """Задача для отправки напоминания пользователю """

    for habit in get_habits():
        message = f' Пора {habit.action} в {habit.time} {habit.place}'
        if habit.user.chat_id:
            bot.send_message(habit.user.chat_id, message)
            habit.last_reminder = timezone.now()
            habit.save()
        else:
            print(f"У пользователя {habit.user} отсутствует chat_id, "
                  "не получилось отправить")
