from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import (RankConfig, Tag, Domain, News)

admin.site.register(RankConfig, SingletonModelAdmin)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'coef']
    search_fields = ['name']
    list_editable = ['coef']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    filter_horizontal = ['tags']

    list_display = ['image_cropped', 'domain', 'pub_date', 'created', 'updated', 'comments', 'views', 'source']
    list_filter = ['pub_date', 'created', 'updated', 'domain']
    fieldsets = (
        ('Links', {'fields': ['domain', 'url'], 'classes': ['full-width']}),
        ('Dates', {'fields': ['pub_date', ('created', 'updated')]}),
        ('Social', {'fields': [('views', 'comments'), 'social']}),
        ('Image', {'fields': ['image', 'image_url']}),
        ('Content', {'fields': ['title', 'author', 'text', 'tags']}),
    )
    readonly_fields = ['created', 'updated', 'image_url']

    def source(self, obj):
        return '<a href="{}" target="_blank">source</a>'.format(obj.url_raw)
    source.allow_tags = True

    def image_cropped(self, obj):
        image_url = 'http://via.placeholder.com/100x100?text=No+image'
        if obj.image:
            image_url = obj.image.url
        return '<img src="{}" width="100" height="100" />'.format(image_url)

    image_cropped.allow_tags = True
    image_cropped.short_description = 'Image'
