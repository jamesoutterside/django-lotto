from django.test import TestCase

from .models import Lottery, Entry
from .factories import UserFactory, LotteryFactory

class LotteryTestCase(TestCase):

    def test_something(self):
        lotto = LotteryFactory.create()


