from django.template.defaultfilters import slugify

import factory
import factory.fuzzy
import datetime
import pytz

import models

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User
        django_get_or_create = ('username',)

    first_name = factory.Sequence(lambda n: "user %03d" % n)
    last_name = factory.Sequence(lambda n: "%03d" % n)
    username = factory.lazy_attribute(lambda o: slugify(o.first_name + '.' + o.last_name))
    email = factory.lazy_attribute(lambda o: o.username + "@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'password')



class LotteryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Lottery

    name = factory.Sequence(lambda n: "Lotto %03d" % n)
    description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do " \
                  "eiusmod tempor incididunt ut labore et dolore magna aliqua." \
                  " Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris " \
                  "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in " \
                  "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla " \
                  "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa " \
                  "qui officia deserunt mollit anim id est laborum." # since django removed webdesign in 19 :/
    is_active_from = factory.fuzzy.FuzzyDateTime(datetime.datetime.now(pytz.UTC) - datetime.timedelta(days=1),
                                                 datetime.datetime.now(pytz.UTC) + datetime.timedelta(days=1))
    is_closed_from = factory.fuzzy.FuzzyDateTime(datetime.datetime.now(pytz.UTC) + datetime.timedelta(days=1),
                                                 datetime.datetime.now(pytz.UTC) + datetime.timedelta(days=7))
    number_of_balls = factory.fuzzy.FuzzyInteger(2, 6)
    max_ball = factory.fuzzy.FuzzyInteger(10, 49)



class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Entry
        django_get_or_create = ('entry_user','entry_for') # hold up unique constraint

    entry_user = factory.Iterator(models.User.objects.filter(is_staff=False))
    balls = factory.lazy_attribute(lambda o: o.entry_for.pick_lucky_dip())

