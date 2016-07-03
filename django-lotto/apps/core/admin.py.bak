from django.contrib import admin
from django.contrib.admin.sites import site
from django.utils.html import escape
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.core.urlresolvers import reverse
from models import Lottery, Entry, User

class ReadOnlyTabularInline(admin.TabularInline):
    show_change_link = True
    extra = 0
    max_num = 0 # so we have no add another on lines

    # disable add/delete on inlines for now
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class VerboseForeignKeyRawIdWidget(ForeignKeyRawIdWidget):
    def label_for_value(self, value):
        key = self.rel.get_related_field().name
        try:
            obj = self.rel.to._default_manager.using(self.db).get(**{key: value})
            change_url = reverse(
                "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.object_name.lower()),
                args=(obj.pk,)
            )
            return '&nbsp;<strong><a href="%s">%s</a></strong>' % (change_url, escape(obj))
        except (ValueError, self.rel.to.DoesNotExist):
            return '???'

class BaseAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        """
            We want no deletes from the admin ATM, we should replace this with a soft delete in time.
        """
        if request.user.is_superuser:
            return True
        else:
            return False

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
            Generic tie in for fk to use linked
        """

        db = kwargs.get('using')
        if db_field.name in self.raw_id_fields:
            kwargs['widget'] = VerboseForeignKeyRawIdWidget(db_field.rel, site)
        elif db_field.name == 'evaluation_form':
            kwargs['empty_label'] = 'No evaluation form assigned'
            kwargs['required'] = False

        return db_field.formfield(**kwargs)

class LotteryAdmin(BaseAdmin):
    list_display = ('name','number_of_balls','max_ball','draw_result','draw_date',
                    'is_active','total_winners','total_entries','manual_draw')
    list_editable = ('is_active',)
    list_filter = ('is_active','draw_date','number_of_balls')
    date_hierarchy = 'date_created'
    search_fields = ('name','description')
    readonly_fields = ('draw_date','draw_result','draw_machine')

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

    def manual_draw(self, obj):
        if not obj.draw_date:
            return '<a href="%(url)s">Manual draw</a>' % {'url':reverse('admin_manual_draw', args=(obj.pk,)),}
        else:
            return '-'
    manual_draw.allow_tags = True

class EntryAdmin(BaseAdmin):
    list_display = ('entry_for','entry_user','balls','winner')
    raw_id_fields = ('entry_for','entry_user')

    def get_queryset(self, request):
        """
            Add in select related for speedup
        """
        return super(EntryAdmin, self).get_queryset(request).select_related('entry_for','entry_user')


class EntryInline(ReadOnlyTabularInline):
    model = Entry
    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return [f.name for f in Entry()._meta.fields]
        else:
            return []


class CustomUserAdmin(UserAdmin):
    inlines = (EntryInline,)
    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return [f.name for f in obj._meta.fields]
        else:
            return []


admin.site.register(Lottery, LotteryAdmin)
admin.site.register(Entry, EntryAdmin)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
