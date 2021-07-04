from celery import shared_task

from .models import Node, Link
from data_api.models import User, Article, Comment

@shared_task(name='sum two numbers')
def add(x, y):
    return x + y