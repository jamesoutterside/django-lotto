from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from models import Lottery, Entry
from forms import EntryForm, BALL_KEY


def index(request):
    bag = {}

    open_lotteries = Lottery.objects.get_active_no_draw()
    bag['open_lotteries'] = open_lotteries

    return render(request, 'core/index.html', bag)

@login_required
def entry(request, lottery_id):
    bag = {}

    lottery = get_object_or_404(Lottery, pk=lottery_id)
    bag['lottery'] = lottery

    try:
        entry = Entry.objects.get(entry_user__username=request.user.username,
                                  entry_for=lottery)
        bag['entry'] = entry
    except Entry.DoesNotExist:
        entry = None

    # can only enter if they haven't already and the lottery is still open
    if not entry and lottery.allows_entry():
        if request.method == 'POST':
            form = EntryForm(request.POST,
                             number_of_balls=lottery.number_of_balls, min_ball=1, max_ball=lottery.max_ball)

            if form.is_valid():
                balls = form.cleaned_data['validated_balls']
                Entry.objects.create(entry_for=lottery, entry_user=request.user, balls=balls)
                messages.success(request, 'Entry placed!')
                return HttpResponseRedirect(reverse('entry',kwargs={'lottery_id':lottery_id}))

        # if a GET (or any other method) we'll create a blank form
        else:
            form = EntryForm(number_of_balls=lottery.number_of_balls, min_ball=1, max_ball=lottery.max_ball)

        bag['form'] = form

    return render(request, 'core/entry.html', bag)
