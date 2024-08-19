import os

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.utils import timezone

from .models import Task
from aiogram import Bot
from aiogram.exceptions import TelegramAPIError


@shared_task
def send_task_notification(task_id, chat_telegram_id, **_kwargs):
    task = Task.objects.get(id=task_id)
    if task.notification_time and task.notification_time <= timezone.now():
        user_msg = task.original_message
        send_text = f'Напоминание об {task}: {user_msg}'
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': send_text
            }
        )

        print(chat_telegram_id)
        if chat_telegram_id:
            bot = Bot(token=os.environ.get('BOT_TOKEN'))

            async def send_telegram_message(chat_id, text):
                try:
                    print('send msg')
                    await bot.send_message(chat_id=chat_id, text=text)
                except TelegramAPIError as e:
                    print(f"Ошибка при отправке сообщения: {e}")

            async_to_sync(send_telegram_message)(chat_telegram_id, send_text)
    else:
        print(f'Task {task_id} is not yet due for notification.')
