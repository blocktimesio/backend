from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.auth import get_user_model
from ..users.models import User as UserModel
from .models import (Tag, Post)

User = get_user_model()  # type: UserModel


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
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


class PostOwnerFilter(SimpleListFilter):
    title = 'By owner'
    parameter_name = 'by_owner'

    class CHOICES:
        MY = 'my'
        TO_ME = 'to_me'

        LOOKUPS = [
            (MY, 'Only my'),
            (TO_ME, 'Assigned to me'),
        ]

    def lookups(self, request, model_admin):
        return self.CHOICES.LOOKUPS

    def queryset(self, request, queryset):
        queryset = queryset.all()
        if self.value() == self.CHOICES.MY:
            queryset = queryset.filter(author=request.user)
        if self.value() == self.CHOICES.TO_ME:
            queryset = queryset.filter(assigned=request.user)
        return queryset


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    filter_horizontal = ['tags']
    radio_fields = {'status': admin.HORIZONTAL}

    list_display = ['name', 'status', 'author', 'created', 'modified']
    list_filter = [PostOwnerFilter, 'status', 'author', 'created', 'modified']

    fieldsets = (
        ('Main', {'fields': ['name', 'slug', 'image', 'pub_date', 'status'], 'classes': ['full-width']}),
        ('Content', {'fields': ['content', 'tags']}),
    )

    def get_prepopulated_fields(self, request, obj=None):
        prepopulated_fields = {'slug': ('name',), }

        if not obj:
            return prepopulated_fields

        is_author = obj.author == request.user
        if obj.locked and not is_author:
            return {}
        if not request.user.is_editor and not is_author:
            return {}

        return prepopulated_fields

    def has_delete_permission(self, request, obj=None):
        if request.user.is_editor:
            return True
        if obj:
            return obj.author == request.user
        return True

    def save_model(self, request, obj: Post, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user

        obj.save()
