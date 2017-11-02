from django.contrib import admin
from django.contrib.auth import get_user_model
from ...users.models import User as UserModel
from ..models import Tag

User = get_user_model()  # type: UserModel


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'author', 'created', 'modified']
    list_filter = ['author', 'created', 'modified']
    search_fields = ['name', 'slug']
    fieldsets = (
        ('Main', {'fields': ('name', 'slug')}),
    )

    def get_prepopulated_fields(self, request, obj=None):
        prepopulated_fields = {'slug': ('name',), }

        if not obj:
            return prepopulated_fields

        is_author = obj.author == request.user
        if not request.user.is_editor and not is_author:
            return {}

        return prepopulated_fields

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return []

        fields = ['name', 'slug']
        is_author = obj.author == request.user
        if not request.user.is_editor and not is_author:
            return fields
        return []

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
