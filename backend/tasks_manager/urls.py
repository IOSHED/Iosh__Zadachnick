from django.urls import path
from .views import TaskListView, TaskManagerView


urlpatterns = [
    path('', TaskManagerView.as_view(), name="home"),
    path('list-tasks', TaskListView.as_view(), name='list_tasks'),
]
