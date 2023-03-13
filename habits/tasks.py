from celery import shared_task
import celery
import requests
from django.conf import settings
from users.models import User


@shared_task
def notify(**kwargs):
    print(kwargs)

