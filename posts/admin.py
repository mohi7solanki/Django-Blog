from django.contrib import admin
from .models import Post, Category
from mptt.admin import DraggableMPTTAdmin

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp', 'updated')
    list_filter = ['timestamp', 'updated']
    search_fields = ['title', 'content']


admin.site.register(Post, PostAdmin)
admin.site.register(Category , DraggableMPTTAdmin)

