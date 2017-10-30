from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.auth import get_user_model
from .filters import PostOwnerFilter
from .post_forms import AdminPostForm
from ...users.models import User as UserModel
from ..models import Post

User = get_user_model()  # type: UserModel


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = AdminPostForm
    filter_horizontal = ['tags']

    list_display = ['name', 'status', 'locked', 'author', 'assigned', 'created', 'modified']
    list_filter = [PostOwnerFilter, 'status', 'locked', 'author', 'assigned', 'created', 'modified']

    fieldsets = (
        ('Main', {'fields': ['name', 'slug', 'image']}),
        ('Content', {'fields': ['content', 'tags']}),
        ('Assigned to', {'fields': ['assigned']}),
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

    def get_readonly_fields(self, request, obj: Post=None):
        if not obj:
            return []

        fields = flatten_fieldsets(self.fieldsets)
        is_author = obj.author == request.user
        if obj.locked and not is_author:
            return fields
        if not request.user.is_editor and not is_author:
            return fields
        return []

    def get_form(self, request, obj=None, **kwargs):
        form = super(PostAdmin, self).get_form(request, obj, **kwargs)
        form.user = request.user
        return form

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

    def save_model(self, request, obj: Post, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user

        # TODO: disable to edit assigned

        obj.save()
