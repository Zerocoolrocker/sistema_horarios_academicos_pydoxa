from django.contrib import admin
from django.contrib.admin.models import LogEntry

import core.models

for modelo in dir(core.models):
    if getattr(core.models, modelo).__class__.__name__ == 'ModelBase' and getattr(core.models, modelo).__name__ != 'User':
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

admin.site.register(LogEntry, LogEntryAdmin)
