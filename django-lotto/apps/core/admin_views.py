from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib import messages

from models import Lottery

@staff_member_required
def manual_draw(request, lottery_id):
    """
        Manual draw call from admin site
    """
    lotto = get_object_or_404(Lottery, pk=lottery_id, draw_date__isnull=True)
    lotto.do_draw()
    messages.success(request, 'Draw completed by %s' % lotto.draw_machine)
    return HttpResponseRedirect(reverse('admin:core_lottery_change', args=(lottery_id,)))

