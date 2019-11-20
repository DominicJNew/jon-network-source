from django.contrib import admin
from .models import Item, Comment
# Register your models here.

def update_urls(modeladmin, request, queryset):
    for item in queryset:
        item.update_url()
        
def twat(modeladmin, request, queryset):
    for item in queryset:
        item.tweet()

def give_title(modeladmin, request, queryset):
    for item in queryset:
        item.title = "The Bible"
        item.save()
        
twat.short_description = 'Twat.'
update_urls.short_description = 'Update URL'

class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'votes', 'views', 'short_desc']
    actions = [update_urls, twat, give_title]  # <-- Add the list action function here

admin.site.register(Item, ItemAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'to_item','body']

admin.site.register(Comment, CommentAdmin)