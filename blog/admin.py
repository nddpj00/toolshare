from django.contrib import admin
from .models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'date',
        'author',
        'slug',
        'thumb',
        'id',
    )


admin.site.register(Article,ArticleAdmin)

