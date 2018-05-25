from datetime import datetime

from django.db import models


class SurvConfiguration(models.Model):
    alarm_state = models.BooleanField(default=True)
    picture_mode = models.BooleanField(default=True)


class AlarmHistory(models.Model):
    date = models.DateTimeField(blank=False)

    @classmethod
    def create(cls, date):
        # date = YYYY_MM_DD_HH:MM:SS
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:10])
        hour = int(date[11:13])
        minute = int(date[14:16])
        second = int(date[17:19])
        timestamp = datetime(year=year,
                             month=month,
                             day=day,
                             hour=hour,
                             minute=minute,
                             second=second)

        history = cls(date=timestamp)

        return history
