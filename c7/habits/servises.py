from django.utils import timezone

from habits.models import Habit


def get_habits():
    """Возвращает список привычек по которым необходима отправка оповещений """

    habits = []
    habits_obj = Habit.objects.all()
    for habit in habits_obj:
        if habit.last_reminder:
            if habit.last_reminder <= timezone.now() - timezone.timedelta(
                    days=habit.periodicity):
                habits.append(habit)
        else:
            if habit.time <= timezone.localtime(timezone.now()).time():
                habits.append(habit)
    return habits


