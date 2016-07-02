from django.test import TestCase
from django.core.management import call_command

from core.factories import UserFactory, LotteryFactory

# coverage run manage.py test && coverage report --include=django-lotto/* -m

class LotteryTestCase(TestCase):
    def setUp(self):
        # user same data as management command for now, plus it needs testing
        call_command('create_test_data')
    
    def test_lottery(self):
        pass


