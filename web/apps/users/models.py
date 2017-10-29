from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'type']

    class TYPE:
        EDITOR = 'ed'
        PUBLISHER = 'pub'

        CHOICES = (
            (EDITOR, 'Editor'),
            (PUBLISHER, 'Publisher'),
        )

    type = models.CharField(max_length=4, default=TYPE.PUBLISHER, choices=TYPE.CHOICES)
    email = models.EmailField(max_length=255, unique=True)

    @property
    def is_editor(self):
        return self.type == self.TYPE.EDITOR

    @property
    def is_publisher(self):
        return self.type == self.TYPE.PUBLISHER

    class Meta:
        app_label = 'users'
