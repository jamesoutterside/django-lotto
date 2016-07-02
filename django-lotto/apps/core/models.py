from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from manager import LotteryManager

class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class Lottery(BaseModel):
    # detail
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    # rules/setup
    number_of_balls = models.IntegerField(help_text='From 1 - 10',
                                          validators=[MaxValueValidator(10), MinValueValidator(1)])
    max_ball = models.IntegerField(help_text='From 1 - 100',
                                   validators=[MaxValueValidator(100), MinValueValidator(1)])

    # simple occurrence/next run fields
    occurrence = models.IntegerField(default=7)
    next_draw = models.DateTimeField()  # on run update from occurrence

    # admin
    is_active = models.BooleanField(default=False)
    is_active_from = models.DateTimeField(auto_now_add=True)

    objects = LotteryManager()


class Entry(BaseModel):
    entry_for = models.ForeignKey(Lottery)
    entry_user = models.ForeignKey(User)
    balls = models.CommaSeparatedIntegerField(max_length=255)
    winner = models.NullBooleanField()

    class Meta:
        unique_together = ('entry_for','entry_user')

