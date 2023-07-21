from django.contrib import admin

from .models import User, Subscribe


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email')
    list_filter = ('username', 'email')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    exclude = ('pk',)
    list_filter = ('user', 'author')
