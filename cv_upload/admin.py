from django.contrib import admin
from .models import CV, Message
from django.urls import reverse
from django.utils.html import format_html

@admin.register(CV)
class CVAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'education_level', 'status', 'rating', 'uploaded_at', 'actions_buttons')
    list_filter = ('status', 'position', 'education_level')
    search_fields = ('name', 'education_discipline')
    
    def actions_buttons(self, obj):
        accept_url = reverse('cv_upload:accept_cv', args=[obj.id])
        reject_url = reverse('cv_upload:reject_cv', args=[obj.id])
        return format_html(
            '<a class="button" href="{}">Accept</a>&nbsp;'
            '<a class="button" href="{}">Reject</a>',
            accept_url, reject_url
        )
    actions_buttons.short_description = 'Actions'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'created_at', 'read')
    list_filter = ('read', 'created_at')
    search_fields = ('subject', 'content')
