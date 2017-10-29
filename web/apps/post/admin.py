from django.contrib import admin
from django.contrib.auth import get_user_model
from ..users.models import User as UserModel
from .models import (Post, Tag)

User = get_user_model()  # type: UserModel


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }

    list_display = ['name', 'slug', 'user', 'created', 'modified']
    list_filter = ['user', 'created', 'modified']
    search_fields = ['name', 'slug']
    fieldsets = (
        ('Main', {'fields': ('name', 'slug')}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(type__in=User.TYPE.EDITORS)
        return super(TagAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_editor:
            return True
        if obj:
            return obj.user == request.user
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_editor:
            return True
        if obj:
            return obj.user == request.user
        return True

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ['tags']
    prepopulated_fields = {'slug': ('name',), }
    fieldsets = (
        ('Main', {'fields': (('name', 'slug'), 'pub_date')}),
        ('Content', {'fields': ('content', 'tags')}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(type__in=User.TYPE.EDITORS)
        return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_list_display(self, request):
        fields = ['name', 'status', 'pub_date', 'created', 'modified']
        if request.user.is_editor:
            fields.insert(2, 'user')
        return fields

    def get_list_filter(self, request):
        fields = ['status', 'pub_date', 'created', 'modified']
        if request.user.is_editor:
            fields.insert(0, 'user')
        return fields

    def has_delete_permission(self, request, obj=None):
        if request.user.is_editor:
            return True
        if obj:
            return obj.user == request.user
        return True

    def has_change_permission(self, request, obj=None):
        if request.user.is_editor:
            return True
        if obj:
            return obj.user == request.user
        return True

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()
