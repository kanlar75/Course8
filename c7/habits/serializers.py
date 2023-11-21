from rest_framework import serializers

from habits.models import Habit
from habits.validators import EstimatedTimeValidator, PeriodicityValidator, \
    ConnectedOrRewardValidator, PleasantConnectedValidator, \
    PleasantConnectedRewardValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор привычки """

    periodicity = serializers.IntegerField(default=1)

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [EstimatedTimeValidator(field='estimated_time'),
                      PeriodicityValidator(field='periodicity'),
                      ConnectedOrRewardValidator(field1='connected_habit',
                                                 field2='reward'),
                      PleasantConnectedValidator(field='connected_habit'),
                      PleasantConnectedRewardValidator(field1='is_pleasant',
                                                       field2='reward',
                                                       field3='connected_habit'
                                                       ),
                      ]
