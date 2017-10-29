from django.contrib.auth.forms import (
    UsernameField,
    UserCreationForm as BaseUserCreationForm

)
from .models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'type']
        field_classes = {'username': UsernameField}
