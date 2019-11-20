from django.contrib import admin

# Register your models here.
from .models import Chat

class ChatAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Chat._meta.fields]

admin.site.register(Chat, ChatAdmin)