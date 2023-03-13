import requests
from django.conf import settings
from users.models import User
from celery import shared_task


@shared_task
def get_chat_id():
    if not_confirmed_users := User.objects.filter(chat_id=None).values_list('telegram_id', flat=True):

        request_link = f'https://api.telegram.org/bot{settings.TELEBOT_TOKEN}/getUpdates'
        r = requests.get(request_link, )
        messages = r.json().get('result')
        unique_users_in_messages = list({v.get('message').get('from').get('username'): v for v in messages}.values())

        for chat_data in unique_users_in_messages:

            if (username := chat_data.get('message').get('from').get('username')) in not_confirmed_users:
                chat_id = chat_data.get('message').get('from').get('id')
                user = User.objects.get(telegram_id=username)
                user.chat_id = chat_id
                user.save()
