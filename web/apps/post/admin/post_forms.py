from django import forms
from django.contrib.auth import get_user_model
from ...users.models import User as UserModel
from ..models import Post

User = get_user_model()  # type: UserModel


class AdminPostForm(forms.ModelForm):
    # assigned_to = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(AdminPostForm, self).__init__(*args, **kwargs)

        if 'assigned' not in self.fields:
            return

        if self.user.is_editor:
            self.fields['assigned'].queryset = User.objects.filter(type__in=User.TYPE.EDITORS)
        if self.user.is_publisher:
            self.fields['assigned'].queryset = User.objects.filter(type=User.TYPE.EDITOR)

        instance = kwargs.get('instance')  # type: Post
        if instance:
            if not self.user.is_publisher or instance.author != self.user:
                if instance.assigned and instance.assigned != self.user:
                    self.fields['assigned'].disabled = True

    class Meta:
        model = Post
        exclude = '__all__'
