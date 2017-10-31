from django.db import models
from django.contrib.auth.models import (AbstractUser, Group)
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class User(AbstractUser):
    REQUIRED_FIELDS = ['email', 'type']

    class TYPE:
        EDITOR = 'ed'
        PUBLISHER = 'pub'
        USER = 'user'

        CHOICES = (
            (EDITOR, 'Editor'),
            (PUBLISHER, 'Publisher'),
            (USER, 'Simple user'),
        )

        EDITORS = [EDITOR, PUBLISHER]

    type = models.CharField(max_length=4, default=TYPE.USER, choices=TYPE.CHOICES)
    email = models.EmailField(max_length=255, unique=True)

    @property
    def is_editor(self):
        return self.type == self.TYPE.EDITOR

    @property
    def is_publisher(self):
        return self.type == self.TYPE.PUBLISHER

    @property
    def is_user(self):
        return self.type == self.TYPE.USER

    class Meta:
        app_label = 'users'


@receiver(pre_save, sender=User)
def pre_create_user(sender, instance: User,  **kwargs):
    if instance.type in User.TYPE.EDITORS:
        instance.is_staff = True
    else:
        instance.is_staff = False


@receiver(post_save, sender=User)
def post_create_user(sender, instance: User, **kwargs):
    g = Group.objects.get(name='Journalists')
    if instance.type in User.TYPE.EDITORS:
        if not instance.groups.filter(id__in=[g.id]).exists():
            g.user_set.add(instance)
    else:
        instance.groups.filter(id__in=[g.id]).delete()
