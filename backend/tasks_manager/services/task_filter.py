
from datetime import timedelta
from django.utils import timezone

from ..models import Task


class TaskFilterService:
    def __init__(self, user):
        self.user = user

    def get_tasks_for_period(self, period):
        start_date, end_date = self._get_date_range(period)
        return self._filter_tasks(start_date, end_date)

    def _get_date_range(self, period):
        today = timezone.now()

        if period == 'day':
            start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
        elif period == 'week':
            start_date = self._get_start_of_week(today)
            end_date = start_date + timedelta(weeks=1)
        elif period == 'month':
            start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = (start_date + timedelta(days=32)).replace(day=1)
        elif period == 'year':
            start_date = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = today.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        else:
            start_date = self._get_start_of_week(today)
            end_date = start_date + timedelta(weeks=1)

        return start_date, end_date

    @staticmethod
    def _get_start_of_week(date):
        start_date = date - timedelta(days=date.weekday())
        return start_date.replace(hour=0, minute=0, second=0, microsecond=0)

    def _filter_tasks(self, start_date, end_date):
        return Task.objects.filter(
            user=self.user,
            start_time__gte=start_date,
            start_time__lt=end_date,
        ).order_by('-create_at')
