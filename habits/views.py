import json
from rest_framework import generics, mixins
from habits.serializers import HabitSerializer, Habits
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule


class ForeignHabitsListView(generics.ListAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habits.objects.filter(is_private=False).exclude(user=self.request.user)


class HabitCreateListView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Habits.objects.all()
        return Habits.objects.filter(user=self.request.user)

    def post(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    def perform_create(self, serializer):
        instance = serializer.save()

        schedule, created = CrontabSchedule.objects.get_or_create(
            hour=instance.time_to_do.strftime('%H'),
            minute=instance.time_to_do.strftime('%M'),
            day_of_week=instance.periodicity,
        )
        PeriodicTask.objects.create(
            crontab_id=schedule.pk,
            name=f'notify {instance.pk}',
            task='habits.task.notify',
            kwargs=json.dumps({
                'owner_pk': self.request.user.pk,
                'habit_pk': instance.pk,
            })
        )


class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Habits.objects.all()
        return Habits.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=self.get_object().periodicity,
            period=IntervalSchedule.DAYS,
        )
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='send notification',
            task='habits.tasks.notify',
        )
        return super().update(request, *args, **kwargs)