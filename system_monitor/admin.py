from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.conf import settings
import django

from .models import Overview
from .utils import get_overview, get_static_overview


class ViewOnlyAmin(admin.ModelAdmin):
    def get_actions(self, request):
        return None

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False








@admin.register(Overview)
class OverviewAdmin(ViewOnlyAmin):
    view_on_site = False
    change_list_template = 'admin/overview_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('api.json/', self.api),
        ]
        return custom_urls + urls

    def api(self, request):
        response = JsonResponse(get_overview(), safe=False)
        return response

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        if request.user.is_superuser:
            if hasattr(response, 'context_data'):
                response.context_data['data'] = get_overview()
                response.context_data['static_overview'] = get_static_overview()
                response.context_data['refresh_interval'] = getattr(
                    settings, 'SYSTEM_MONITOR_REFRESH_INTERVAL', 5000
                )
        return response

    class Media:
        js = (
            'system_monitor/js/index.js',
        )
        css = () # No custom CSS needed for now, mermaid.css is removed
