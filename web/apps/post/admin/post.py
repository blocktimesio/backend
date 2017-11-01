from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin.utils import flatten_fieldsets
from django.contrib.auth import get_user_model
from django.http import (HttpResponse, HttpResponseForbidden)
from django.shortcuts import get_object_or_404
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
        ('Main', {'fields': ['name', 'slug', 'image'], 'classes': ['full-width']}),
        ('Content', {'fields': ['content', 'tags']}),
        ('Assigned to', {'fields': ['assigned'], 'classes': ['full-width']}),
    )

    def get_urls(self):
        urls = super(PostAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>\d+)/change/lock/?$', self.lock_post, name='admin_post_lock'),
        ]
        return my_urls + urls

    def lock_post(self, request, pk):
        if request.user.type not in User.TYPE.EDITORS:
            return HttpResponseForbidden()

        post = get_object_or_404(Post, pk=pk)  # type: Post

        if request.user.is_editor:
            post.locked = not post.locked
            post.save()
            return HttpResponse(status=202)

        if request.user.is_publisher:
            if request.user == post.author:
                if not post.assigned or request.user == post.assigned:
                    post.locked = not post.locked
                    post.save()
                    return HttpResponse(status=202)
                else:
                    return HttpResponseForbidden()
            else:
                return HttpResponseForbidden()

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

        if request.user.is_editor:
            if obj.assigned and obj.assigned != request.user and obj.locked:
                return fields

        if request.user.is_publisher:
            # Not author
            if obj.author != request.user:
                return fields

            # Assigned to other
            if obj.assigned and obj.assigned != request.user:
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

        if 'assigned' in form.changed_data:
            obj.locked = False

        obj.save()

    class Media:
        js = ['admin/js/toggle-post-lock.js']
        css = {
            'all': ('admin/css/styles.css',),
        }
