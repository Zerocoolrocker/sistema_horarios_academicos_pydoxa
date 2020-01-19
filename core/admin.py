from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.admin.utils import quote
from django.contrib.admin.views.main import ChangeList

import core.models

for modelo in dir(core.models):
    if getattr(core.models, modelo).__class__.__name__ == 'ModelBase' and getattr(core.models, modelo).__name__ not in ['User', 'Proyecto']:
        try:
            admin.site.register(getattr(core.models, modelo))
        except:
            pass

class LogEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('content_type',
        'user',
        'action_time',
        'object_id',
        'object_repr',
        'action_flag',
        'change_message'
    )
    list_display = ('action_flag', 'action_time', 'user', 'change_message', 'object_repr', 'object_id')


    def has_delete_permission(self, request, obj=None):
        return False

    # def get_actions(self, request):
    #     actions = super(LogEntryAdmin, self).get_actions(request)
    #     del actions['delete_selected']
    #     return actions


class ProyectoChangeList(ChangeList):
    def url_for_result(self, result):
        return '/proyectodnd/%d/' % (quote(result.pk))

    def get_model(self):
        return self.model.__name__

class ProyectoModelAdmin(admin.ModelAdmin):
    def get_changelist(self, request, **kwargs):
        return ProyectoChangeList



admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(core.models.Proyecto, ProyectoModelAdmin)
