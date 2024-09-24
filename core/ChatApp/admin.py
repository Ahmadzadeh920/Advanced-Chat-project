from django.contrib import admin
from .models import ChatGroup, GroupMessage , GroupMember
# Register your models here.

admin.site.register(ChatGroup)
admin.site.register(GroupMessage)
admin.site.register(GroupMember)
