from django import forms
from django.contrib import admin
from redactor.widgets import RedactorEditor
from .models import Flatpage


class FlatpageAdminForm(forms.ModelForm):
    class Meta:
        model = Flatpage
        fields = '__all__'
        widgets = {
           'content': RedactorEditor(),
        }


@admin.register(Flatpage)
class FlatpageAdmin(admin.ModelAdmin):
    form = FlatpageAdminForm
    prepopulated_fields = {'slug': ['title']}

    list_display = ['title', 'slug', 'is_show']
    list_editable = ['is_show']
    search_fields = ['title', 'slug', 'content']
    fields = ['title', 'slug', 'is_show', 'content']
