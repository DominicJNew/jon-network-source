from django.contrib import admin
from .models import Link

# Register your models here.

def update_domains(modeladmin, request, queryset):
    for item in queryset:
        item.update_domain()
        
update_domains.short_description = 'Update Domains'

class LinkAdmin(admin.ModelAdmin):
    list_display = ['url', 'domain', 'title']
    actions = [update_domains]
    
admin.site.register(Link, LinkAdmin)