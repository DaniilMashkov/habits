from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json


def create_task(serializer):
    instance = serializer.save()

    schedule, created = CrontabSchedule.objects.get_or_create(
        hour=instance.time_to_do.strftime('%H'),
        minute=instance.time_to_do.strftime('%M'),
        day_of_week=instance.periodicity,
    )
    PeriodicTask.objects.get_or_create(
        crontab_id=schedule.pk,
        name=f'notify {instance.pk}',
        task='habits.tasks.notify',
        kwargs=json.dumps({
            'user_chat_id': instance.user.chat_id,
            'habit_pk': instance.pk,
        })
    )