from django.contrib import admin

from .models import Img

def format_votes(modeladmin, request, queryset):
    for item in queryset:
        item.voted = ''
        item.save()

format_votes.short_description = 'Format Dem Votes'

class ImgAdmin(admin.ModelAdmin):
    list_display = ['title', 'clicks', 'impressions', 'votes', 'sender']
    actions = [format_votes]

admin.site.register(Img, ImgAdmin)