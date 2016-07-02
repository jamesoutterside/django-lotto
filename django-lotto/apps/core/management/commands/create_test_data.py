from django.core.management.base import BaseCommand, CommandError
from core.models import Lottery
from core.factories import UserFactory, LotteryFactory, EntryFactory

class Command(BaseCommand):
    help = 'Creates some test data for the site'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('All users created with password - password'))

        # CREATE USERS

        # create admin user
        UserFactory.create(username='super', is_superuser=True, is_staff=True)
        self.stdout.write(self.style.SUCCESS('Superuser username: super'))

        UserFactory.create(username='admin', is_superuser=False, is_staff=True)
        self.stdout.write(self.style.SUCCESS('Staff username: Admin'))

        # create 100 standard users
        UserFactory.create_batch(30)
        self.stdout.write(self.style.SUCCESS('100 Random users created'))

        # CREATE LOTTOS

        # create random
        LotteryFactory.create_batch(2, is_active=True)

        # create some random active 3 ball lotteries
        LotteryFactory.create_batch(10, number_of_balls=3, is_active=True)

        # create some inactive
        LotteryFactory.create_batch(5, number_of_balls=3, is_active=False)

        self.stdout.write(self.style.SUCCESS('Test data created!'))


        # CREATE ENTRIES
        lottos = Lottery.objects.filter()

        EntryFactory.create_batch(100, entry_for=lottos[0])
        EntryFactory.create_batch(100, entry_for=lottos[1])
        EntryFactory.create_batch(100, entry_for=lottos[2])

        # draw some lottos
        lottos[0].do_draw(machine='arthur')
        lottos[1].do_draw(machine='guinevere')
        lottos[2].do_draw(machine='cheat')


