from django.shortcuts import render

from models import Lottery

def index(request):
    bag = {}

    open_lotteries = Lottery.objects.get_active_no_draw()
    bag['open_lotteries'] = open_lotteries

    return render(request, 'core/index.html', bag)