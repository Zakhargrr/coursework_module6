from django.contrib import admin

from blogs.models import Blog


# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'views_count', 'published_at')
