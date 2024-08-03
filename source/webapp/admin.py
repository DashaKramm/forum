from django.contrib import admin

from webapp.models import Topic


# Register your models here.
class TopicAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'created_at']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'content']
    fields = ['title', 'content', 'created_at']
    readonly_fields = ['author', 'created_at', 'updated_at']


admin.site.register(Topic, TopicAdmin)
