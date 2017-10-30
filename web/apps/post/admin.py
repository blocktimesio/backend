from django.contrib import admin
from django.contrib.auth import get_user_model
from .admin_filters import PostOwnerFilter
from ..users.models import User as UserModel
from .models import (Post, Tag)

User = get_user_model()  # type: UserModel


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }

    list_display = ['name', 'slug', 'author', 'created', 'modified']
    list_filter = ['author', 'created', 'modified']
    search_fields = ['name', 'slug']
    fieldsets = (
        ('Main', {'fields': ('name', 'slug')}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['queryset'] = User.objects.filter(type__in=User.TYPE.EDITORS)
        return super(TagAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if request.user.is_editor:
            return True
        if obj:
            return obj.author == request.user
        return True

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ['tags']
    prepopulated_fields = {'slug': ('name',), }

    list_display = ['name', 'status', 'locked', 'author', 'assigned', 'created', 'modified']
    list_filter = [PostOwnerFilter, 'status', 'locked', 'author', 'assigned', 'created', 'modified']

    fieldsets = (
        ('Main', {'fields': (('name', 'slug'), 'pub_date')}),
        ('Content', {'fields': ('content', 'tags')}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'author':
            kwargs['queryset'] = User.objects.filter(type__in=User.TYPE.EDITORS)
        if db_field.name == 'assigned':
            kwargs['queryset'] = User.objects.filter(type__in=User.TYPE.EDITORS)
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_editor:
            return True
        if obj:
            return obj.author == request.user
        return True

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()
