from django.db import models

import datetime

class LotteryQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def active_from(self):
        return self.filter(is_active_from__gte=datetime.datetime.now())

class LotteryManager(models.Manager):
    def get_queryset(self):
        return LotteryQuerySet(self.model, using=self._db)

    def get_active(self):
        """
            Get active lotteries
        """
        qs = self.get_queryset()
        qs = qs.active()
        qs = qs.active_from()

        return qs


    def draw(self):
        pass
