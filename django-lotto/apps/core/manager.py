from django.db import models

import datetime
import random
import logging

logger = logging.getLogger(__name__)

class LotteryQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def active_from(self):
        return self.filter(is_active_from__lte=datetime.datetime.now())

    def not_drawn(self):
        return self.filter(draw_date__isnull=True)

    def is_drawn(self):
        return self.exclude(draw_date__isnull=True)

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

    def get_active_no_draw(self):
        qs = self.get_active()
        qs = qs.not_drawn()

        return qs


    def get_active_drawn(self):
        qs = self.get_active()
        qs = qs.is_drawn()

        return qs


    def draw(self, lottery, machine):
        """
            Draw the lottery, use specified machine
        """
        result = []

        try:
            ball_machine = getattr(self, 'draw_%s' % machine)
            balls = ball_machine(lottery=lottery)
            logger.debug('Draw with balls %s' % balls)
        except AttributeError:
            logger.warning('Attempt to draw with not implemented machine')

        while len(result) < lottery.number_of_balls:
            result.append(balls.pop(random.randrange(len(balls))))

        sorted_result = sorted(result)
        return ','.join([str(s) for s in sorted_result])

    def draw_arthur(self, lottery):
        balls = range(1, int(lottery.max_ball))
        return balls

    def draw_guinevere(self, lottery):
        return self.draw_arthur(lottery=lottery) # for now...

    def draw_cheat(self, lottery):
        """
            Picks a random entry to win
        """
        entry = lottery.entry_set.filter().order_by('?').first()

        if entry:
            return entry.get_balls
        else:
            return []
