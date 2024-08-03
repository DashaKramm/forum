from django.contrib import admin
from django.contrib.auth import get_user_model

# Register your models here.
User = get_user_model()


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'avatar']
    list_display_links = ['id', 'username']
    search_fields = ['username']


admin.site.register(User, CustomUserAdmin)
