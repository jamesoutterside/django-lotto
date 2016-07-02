from django.contrib import admin

from models import Lottery, Entry


class LotteryAdmin(admin.ModelAdmin):
    list_display = ('name','number_of_balls','max_ball','draw_result','draw_date',
                    'is_active','is_active_from','is_closed_from')
    list_editable = ('is_active',)
    list_filter = ('is_active','draw_date','number_of_balls')
    date_hierarchy = 'date_created'
    search_fields = ('name','description')


class EntryAdmin(admin.ModelAdmin):
    list_display = ('entry_for','entry_user','balls','winner')
    raw_id_fields = ('entry_for','entry_user')

    def get_queryset(self, request):
        """
            Add in select related for speedup
        """
        return super(EntryAdmin, self).get_queryset(request).select_related('entry_for','entry_user')


admin.site.register(Lottery, LotteryAdmin)
admin.site.register(Entry, EntryAdmin)
