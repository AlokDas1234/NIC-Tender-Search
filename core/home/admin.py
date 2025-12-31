from django.contrib import admin

from .models import SiteName,Client,TenderResults


@admin.register(SiteName)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('state_name', 'site_url')
    search_fields = ('state_name',)
    list_filter = ('state_name',)



@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('state_name', 'site_url')
    search_fields = ('state_name',)
    list_filter = ('state_name',)

class TenderResultsAdmin(admin.ModelAdmin):
    list_display = ('state_name', 'site_link')
    search_fields = ('state_name',)



