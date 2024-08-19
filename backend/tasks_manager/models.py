from django.db import models

from accounts.models import CustomUser
from .parser import TaskParser


class UserMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    original_message = models.TextField()

    def __str__(self):
        return self.original_message


class TaskManager(models.Manager):
    def create_from_message(self, user_message):
        task_info = TaskParser(user_message.original_message).parse()
        return self.create(
            user=user_message.user,
            name=task_info['name_task'],
            description=task_info.get('description'),
            start_time=task_info['start_task'],
            notification_time=task_info.get('notification'),
            original_message=user_message
        )


class Task(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    notification_time = models.DateTimeField(null=True, blank=True)
    original_message = models.OneToOneField(UserMessage, on_delete=models.CASCADE)
    create_at = models.DateField(auto_now_add=True)

    objects = TaskManager()

    def __str__(self):
        return self.name
