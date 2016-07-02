from django.contrib import admin
from django.core.urlresolvers import reverse
from models import Lottery, Entry


class BaseAdmin(admin.ModelAdmin):
    pass

class LotteryAdmin(BaseAdmin):
    list_display = ('name','number_of_balls','max_ball','draw_result','draw_date',
                    'is_active','total_winners','total_entries')
    list_editable = ('is_active',)
    list_filter = ('is_active','draw_date','number_of_balls')
    date_hierarchy = 'date_created'
    search_fields = ('name','description')

    def total_winners(self, obj):
        return '<a href="%(url)s?entry_for=%(pk)s&winner=1">' \
               '%(count)s</a>' % {'url':reverse('admin:core_entry_changelist'),
                                  'pk': obj.pk,
                                  'count':obj.entry_set.filter(winner=True).count()}
    total_winners.allow_tags = True

    def total_entries(self, obj):
        return '<a href="%(url)s?entry_for=%(pk)s">' \
               '%(count)s</a>' % {'url':reverse('admin:core_entry_changelist'),
                                  'pk': obj.pk,
                                  'count':obj.entry_set.filter().count()}
    total_entries.allow_tags = True

class EntryAdmin(BaseAdmin):
    list_display = ('entry_for','entry_user','balls','winner')
    raw_id_fields = ('entry_for','entry_user')

    def get_queryset(self, request):
        """
            Add in select related for speedup
        """
        return super(EntryAdmin, self).get_queryset(request).select_related('entry_for','entry_user')

admin.site.register(Lottery, LotteryAdmin)
admin.site.register(Entry, EntryAdmin)
