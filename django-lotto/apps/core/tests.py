from django.test import TestCase, Client
from django.core.management import call_command
from django.core.urlresolvers import reverse

from core.factories import UserFactory, LotteryFactory, EntryFactory
from core.models import Lottery, Entry
from core.forms import BALL_KEY

import datetime
import pytz
import random

# coverage run manage.py test && coverage report --include=django-lotto/* -m

class LotteryTestCase(TestCase):
    def setUp(self):
        pass
        # user same data as management command for now, plus it needs testing
        # call_command('create_test_data')

    def test_lottery(self):
        now = datetime.datetime.now(pytz.UTC)
        tomorrow = datetime.datetime.now(pytz.UTC) + datetime.timedelta(days=1, )
        active_not_drawn = LotteryFactory.create(is_active=True, is_closed_from=tomorrow, is_active_from=now)
        active_drawn = LotteryFactory.create(is_active=True, draw_date=now, draw_result='1,2',
                                             is_closed_from=tomorrow, is_active_from=now)

        self.assertEqual(True, active_not_drawn.is_active)
        self.assertIn(active_not_drawn, Lottery.objects.get_active_no_draw())
        self.assertIn(active_drawn, Lottery.objects.get_active_drawn())
        self.assertNotIn(active_drawn, Lottery.objects.get_active_no_draw())

        # do draw
        active_not_drawn.do_draw()
        self.assertIn(active_not_drawn, Lottery.objects.get_active_drawn())

    def test_entry(self):
        user = UserFactory.create()
        now = datetime.datetime.now(pytz.UTC)
        tomorrow = datetime.datetime.now(pytz.UTC) + datetime.timedelta(days=1, )
        active_not_drawn = LotteryFactory.create(is_active=True, is_closed_from=tomorrow, is_active_from=now)
        entry = EntryFactory.create(entry_for=active_not_drawn, entry_user=user)

        self.assertEqual(None, entry.winner)
        # test the cheat draw , should pick entry as its the only one!
        active_not_drawn.do_draw(machine='cheat')
        print '**%s' % entry.balls
        print '##%s' % active_not_drawn.draw_result
        

        self.assertEqual(True, Entry.objects.get(id=entry.pk).winner)

    def test_views(self):
        client = Client()

        user = UserFactory.create(username='tester', password='tester')
        client.login(username=user.username, password='tester')

        now = datetime.datetime.now(pytz.UTC)
        tomorrow = datetime.datetime.now(pytz.UTC) + datetime.timedelta(days=1, )

        response = client.get(reverse('index'))
        self.assertEqual(200,response.status_code)

        response = client.get(reverse('passed'))
        self.assertEqual(200,response.status_code)

        active_not_drawn = LotteryFactory.create(is_active=True, is_closed_from=tomorrow, is_active_from=now)
        response = client.get(reverse('entry', args=(active_not_drawn.pk,)))
        self.assertEqual(200,response.status_code)

        post_var = {}
        balls = range(1, int(active_not_drawn.max_ball))
        i = 1
        while len(post_var.values()) < active_not_drawn.number_of_balls:
            post_var['%s%s' % (BALL_KEY,i)] = balls.pop(random.randrange(len(balls)))
            i += 1
        print post_var
        client.post(reverse('entry', args=(active_not_drawn.pk,)), post_var)
        self.assertIn(active_not_drawn.pk, Entry.objects.filter(entry_user=user).values_list('pk',flat=True))

        response = client.get(reverse('user_index'))
        self.assertEqual(200,response.status_code)





