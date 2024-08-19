"""
Входное сообщение: "Сходить в парикмхерскую в 16:00. Напомни за 1 час. Я хочу сделать маникюр."

Выход:
{
  "name_task": "Сходить в парикмахерскую",
  "description": "Я хочу сделать маникюр",
  "start_task": "12.08.2024 16:00.0.0",
  "notification": "12.08.2024 15:00.0.0"
}

Входное сообщение: "10.10.2024 Полить цветы."

Выход:
{
  "name_task": "Полить цветы",
  "description": None,
  "start_task": "10.10.2024 08:00.0.0",
  "notification": "10.10.2024 08:00.0.0"
}

Входное сообщение: "Встреча в 14:30 05 ноября, напомни за 30 мин."

Выход:
{
  "name_task": "Встреча",
  "description": None,
  "start_task": "05.11.2024 14:30.0.0",
  "notification": "05.11.2024 14:00.0.0"
}

Входное сообщение: "Сделать домашку в 18:00 25 декабря."

Выход:
{
  "name_task": "Сделать домашку",
  "description": None,
  "start_task": "25.12.2024 18:00.0.0",
  "notification": "25.12.2024 16:00.0.0"
}

Входное сообщение: "В 09:00 01 января, напомнить за 1 час."

Выход:
{
  "name_task": "В 09:00",
  "description": None,
  "start_task": "01.01.2024 09:00.0.0",
  "notification": "01.01.2024 08:00.0.0"
}

Входное сообщение: "Позвонить врачу в 11:00 30 августа."

Выход:
{
  "name_task": "Позвонить врачу",
  "description": None,
  "start_task": "30.08.2024 11:00.0.0",
  "notification": "30.08.2024 11:00.0.0"
}
"""

import re
from datetime import datetime, timedelta, date, time
from typing import Optional, Tuple, List
from django.utils import timezone
import dateparser
from symspellpy import Verbosity, SymSpell


class TaskParser:
    def __init__(self, message):
        self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        self.sym_spell.load_dictionary('frequency_dictionary_ru.txt', term_index=0, count_index=1)
        self.message = self._correct_spelling(message).lower()
        self.current_date = timezone.now()

    def _correct_spelling(self, message):
        corrected_message = []
        for word in message.split():
            suggestions = self.sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
            if suggestions:
                corrected_message.append(suggestions[0].term)
            else:
                corrected_message.append(word)
        return " ".join(corrected_message)

    def parse(self):
        name = self._extract_name()
        start_time, notification_time = self._extract_start_and_notification_time()
        description = self._extract_description()

        return {
            "name_task": name,
            "description": description,
            "start_task": start_time,
            "notification": notification_time,
        }

    def _extract_name(self) -> str:
        name_patterns = [
            r'(.*?)\s(?:к|в|на)\s(?:\d{1,2}:\d{2}|\d{1,2}\s\w+|\d{2}\.\d{2}\.\д{4})',
            r'(?:планирую|надо сделать|собираюсь)\s+(.*?)(?=\s(?:к|в|на|до|время|срок))',
        ]
        for pattern in name_patterns:
            name_match = re.search(pattern, self.message)
            if name_match:
                return name_match.group(1).strip()
        return self.message.split(' ')[0]

    def _extract_start_and_notification_time(self) -> Tuple[datetime, Optional[datetime]]:
        dates = self._extract_task_date()
        times = self._extract_task_time()

        print(dates)
        print(times)

        task_date = dates[0] or self.current_date.date()
        task_time = times[0] or time(hour=8, minute=0)
        start_task = timezone.make_aware(datetime.combine(task_date, task_time))

        notification_date = dates[-1] or self.current_date.date()
        notification_time = times[-1] or time(hour=8, minute=0)
        notification_time = timezone.make_aware(datetime.combine(notification_date, notification_time))
        print(f'notification_time -> {notification_time}')
        if len(times) == 1 and len(dates) == 1:
            notification_time = start_task - timedelta(hours=2)
        if notification_time is None:
            notification_time = start_task - timedelta(hours=2)
        if self._contains_no_remind():
            notification_time = None

        print(start_task, notification_time)
        return start_task, notification_time

    def _extract_task_date(self) -> List[Optional[date]]:
        res = []
        date_strings = self._search_date_string()
        for date_string in date_strings:
            if date_string:
                parsed_date = dateparser.parse(date_string, settings={'RELATIVE_BASE': self.current_date})
                res.append(parsed_date.date() if parsed_date else None)
        return res if len(res) > 0 else None

    def _extract_task_time(self) -> List[Optional[time]]:
        time_list = []
        time_pattern = re.compile(r'(\d{1,2}:\d{2})')
        time_matches = time_pattern.findall(self.message)

        for time_str in time_matches:
            try:
                parsed_time = datetime.strptime(time_str, '%H:%M').time()
                time_list.append(parsed_time)
            except ValueError:
                continue

        return time_list if len(time_list) > 0 else None

    def _extract_notification_time(self, task_date: date) -> Optional[datetime]:
        notification_pattern = re.compile(r'напомни(?:\sза|в)\s(\d{1,2}:\d{2})')
        notification_match = notification_pattern.search(self.message)
        if notification_match:
            notification_time = datetime.strptime(notification_match.group(1), '%H:%M').time()
            return timezone.make_aware(datetime.combine(task_date, notification_time))
        return None

    def _extract_description(self) -> Optional[str]:
        description_pattern = re.compile(r'(?:буду\sделать|что-то\sдругое|собираюсь|)(.*)', re.IGNORECASE)
        description_match = description_pattern.search(self.message)
        if description_match and description_match.group(1):
            return description_match.group(1).strip()

        if '.' in self.message:
            return self.message.split('.')[-1].strip()

        return None

    def _should_remind_user(self) -> bool:
        return not self._contains_no_remind()

    def _contains_no_remind(self) -> bool:
        return any(phrase in self.message for phrase in ["не надо напоминать", "не напоминать"])

    def _search_date_string(self) -> List[Optional[str]]:
        res = []
        relative_date_pattern = re.compile(r'(сегодня|завтра|послезавтра|через\s\d+\sдн(?:я|ей))')
        absolute_date_pattern = re.compile(r'(\d{1,2}\s\w+|\d{2}\.\d{2}\.\d{4})')
        for pattern in [relative_date_pattern, absolute_date_pattern]:
            date_match = pattern.search(self.message)
            if date_match:
                res.append(date_match.group(1))
        return res if len(res) > 0 else None
