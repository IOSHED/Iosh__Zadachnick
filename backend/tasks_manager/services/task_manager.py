import logging
from pprint import pprint

from django.template.loader import render_to_string
from django.http import HttpResponse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from ..models import Task
from ..tasks import send_task_notification

logger = logging.getLogger(__name__)


class TaskManagerService:
    def __init__(self, user):
        self.user = user

    def create_task_from_message(self, user_message):
        try:
            self._assign_user_to_message(user_message)
            task = self._create_task(user_message)
            chat_telegram_id = self.user.chat_id
            print(chat_telegram_id)
            self._schedule_notification(task, chat_telegram_id)
            self._notify_channels(task)
            return task

        except Exception as e:
            logger.error(f'Error while saving task: {e}')
            return None

    def _assign_user_to_message(self, user_message):
        user_message.user = self.user
        user_message.save()

    @staticmethod
    def _create_task(user_message):
        task = Task.objects.create_from_message(user_message)
        logger.info(f'Task created: {task}')
        return task

    @staticmethod
    def _schedule_notification(task, chat_telegram_id):
        if task.notification_time:
            send_task_notification.apply_async((task.id, chat_telegram_id), eta=task.notification_time)

    @staticmethod
    def _notify_channels(task):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': f'Задача создана: {task}'
            }
        )

    @staticmethod
    def render_task_html(task):
        task_html = render_to_string('tasks/partials/task_item.html', {'task': task})
        return HttpResponse(task_html, content_type='text/html')
