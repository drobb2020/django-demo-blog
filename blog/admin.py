from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Category, Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'slug', 'author', 'status')
    prepopulated_fields = {
        "slug": ("title",),
    }


admin.site.register(Category)

admin.site.register(Comment, MPTTModelAdmin)