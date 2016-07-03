from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from manager import LotteryManager

import random
import datetime
import logging

logger = logging.getLogger(__name__)

class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Lottery(BaseModel):
    # detail
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    prize = models.CharField(max_length=255)

    # rules/setup
    number_of_balls = models.PositiveSmallIntegerField(help_text='From 1 - 10',
                                                       validators=[MaxValueValidator(10), MinValueValidator(1)])
    max_ball = models.PositiveSmallIntegerField(help_text='From 1 - 100',
                                                validators=[MaxValueValidator(100), MinValueValidator(1)])

    # draw details
    draw_result = models.CommaSeparatedIntegerField(max_length=255, null=True, blank=True)
    draw_date = models.DateTimeField(null=True, blank=True)
    draw_machine = models.CharField(max_length=255, null=True, blank=True)

    # admin
    is_active = models.BooleanField(default=False, help_text='Display on site')
    is_active_from = models.DateTimeField(help_text='When to display on site from')
    is_closed_from = models.DateTimeField(help_text='When entries are closed from')

    objects = LotteryManager()

    class Meta:
        verbose_name_plural = 'Lotteries'
        ordering = ('date_created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('entry', kwargs={'lottery_id':self.pk})

    def allows_entry(self):
        now = timezone.now()
        if self.is_active and self.is_active_from < now and self.is_closed_from > now and not self.draw_date:
            return True
        else:
            return False

    def pick_lucky_dip(self):
        """
            Do a lucky dip, for testing but could be front end
        """
        balls = range(1, int(self.max_ball))
        lucky_dip = []

        while len(lucky_dip) < self.number_of_balls:
            lucky_dip.append(balls.pop(random.randrange(len(balls))))

        return ','.join([str(s) for s in sorted(lucky_dip)])

    def do_draw(self, machine='arthur'):
        """
            Draw the lottery and set relevent fields
        """
        result = Lottery.objects.draw(lottery=self, machine=machine)
        self.draw_result = result
        self.draw_date = datetime.datetime.now()
        self.draw_machine = machine
        self.save()

        # update winners
        winners = Entry.objects.filter(balls=result)
        if winners:
            logger.info('Winner(s) found for %s' % self.pk)
            winners.update(winner=True)

        # update losers
        losers = Entry.objects.exclude(pk__in=winners.values_list('pk',flat=True))
        losers.update(winner=False)

        return result, winners


@python_2_unicode_compatible
class Entry(BaseModel):
    entry_for = models.ForeignKey(Lottery)
    entry_user = models.ForeignKey(User)
    balls = models.CommaSeparatedIntegerField(max_length=255)
    winner = models.NullBooleanField()

    class Meta:
        unique_together = ('entry_for','entry_user')
        verbose_name_plural = 'Entries'

    @property
    def get_balls(self):
        return self.balls.split(',')

    def __str__(self):
        return '%s for %s' % (self.entry_user, self.entry_for)
