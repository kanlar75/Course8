from rest_framework.exceptions import ValidationError

from habits.models import Habit


class PeriodicityValidator:
    """ "Проверка периодичности привычки """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        periodicity = dict(value).get(self.field)
        if periodicity:
            if periodicity == 0:
                raise ValidationError(
                    'Периодичность привычки не может равняться нулю!')
            if int(periodicity) > 7:
                raise ValidationError('Нельзя выполнять привычку реже,'
                                      'чем 1 раз в 7 дней')
            return True


class EstimatedTimeValidator:
    """Проверка на выполнение привычки(должно быть не более 120 секунд) """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        estimated_time = (dict(value).get(self.field))
        if estimated_time:
            if int(estimated_time) <= 120:
                return True
            else:
                raise ValidationError('Время выполнения привычки не должно '
                                      'быть более 120 секунд.')


class ConnectedOrRewardValidator:
    """Проверка на одновременный выбор связанной привычки и указания
    вознаграждения"""

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        connected_habit = bool(dict(value).get(self.field1))
        reward = bool(dict(value).get(self.field2))

        if connected_habit and reward:
            raise ValidationError("У привычки не может быть одновременно "
                                  "вознаграждения и связанной привычки")


class PleasantConnectedValidator:
    """В связанные привычки могут попадать только привычки с признаком
    приятной привычки."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        connected_habit = dict(value).get(self.field)
        if connected_habit:
            habit = Habit.objects.get(pk=connected_habit.id)
            if not habit.is_pleasant:
                raise ValidationError(
                    "Связанная привычка должна быть приятной")


class PleasantConnectedRewardValidator:
    """У приятной привычки не может быть вознаграждения или связанной
    привычки."""

    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def __call__(self, value):
        is_pleasant = dict(value).get(self.field1)
        reward = bool(dict(value).get(self.field2))
        connected_habit = bool(dict(value).get(self.field3))

        if is_pleasant and reward or is_pleasant and connected_habit:
            raise ValidationError(
                "У приятной привычки не может быть "
                "вознаграждения или связанной привычки.")
