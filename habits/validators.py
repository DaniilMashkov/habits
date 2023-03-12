from rest_framework import serializers


class HabitValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reward = value.get('reward')
        related_habit = value.get('related_habit')
        is_related = value.get('is_related')

        if related_habit and reward:
            raise serializers.ValidationError('Only one value might be set: "related_habit" or "reward"')

        if not related_habit and not reward and not is_related:
            raise serializers.ValidationError('One value must be set at least: "related habit" or "reward"')

        if is_related and reward:
            raise serializers.ValidationError('Related habit can`t has reward')

        if related_habit and is_related:
            raise serializers.ValidationError('Related habit can not has another habit')
