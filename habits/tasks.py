from celery import shared_task
import requests
from django.conf import settings
from habits.models import Habits


@shared_task
def notify(**kwargs):
    habit = Habits.objects.get(pk=kwargs.get('habit_pk'))

    request_link = f'https://api.telegram.org/bot{settings.TELEBOT_TOKEN}/sendMessage'
    requests.post(request_link, {
        'chat_id': kwargs.get('user_chat_id'),
        'text': f'It`s time for {habit.action} in {habit.place_to_do} to get {habit.reward or habit.related_habit}'
    })

