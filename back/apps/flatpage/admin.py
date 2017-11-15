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

    list_display = ['title', 'url', 'is_show']
    list_editable = ['is_show']
    search_fields = ['title', 'url', 'content']
    fields = ['url', 'title', 'is_show', 'content']
