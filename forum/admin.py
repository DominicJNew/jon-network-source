from django.contrib import admin
from .models import Forum, Reply

# Register your models here.

def update_url(modeladmin, request, queryset):
    for item in queryset:
        item.update_url()

update_url.short_description = "UPdaTE URLZ"

class ForumAdmin(admin.ModelAdmin):
    list_display = ['title', 'sender', 'votes', 'views']
    actions = [update_url,]

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['sender', 'body', 'post_id']

admin.site.register(Forum, ForumAdmin)
admin.site.register(Reply, ReplyAdmin)