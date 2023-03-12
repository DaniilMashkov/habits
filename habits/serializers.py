from habits.models import Habits
from habits.validators import HabitValidator
from rest_framework import serializers


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habits
        fields = '__all__'
        validators = [HabitValidator(field='model')]
