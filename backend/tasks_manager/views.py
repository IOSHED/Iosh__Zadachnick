from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from telegram_bot.models import UserTelegram
from .forms import UserMessageForm

from .models import Task
from .services.task_filter import TaskFilterService
from .services.task_manager import TaskManagerService


class TaskManagerView(LoginRequiredMixin, FormView):
    form_class = UserMessageForm
    template_name = 'tasks/tasks.html'
    login_url = reverse_lazy('login-user')

    def form_valid(self, form):
        user_message = form.save(commit=False)
        task_manager = TaskManagerService(self.request.user)
        task = task_manager.create_task_from_message(user_message)
        response = task_manager.render_task_html(task)
        return response if response else self.form_invalid(form)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    login_url = reverse_lazy('login-user')
    context_object_name = 'tasks'

    def get_queryset(self):
        period = self.request.GET.get('period', 'week')
        task_filter = TaskFilterService(self.request.user)
        return task_filter.get_tasks_for_period(period)
