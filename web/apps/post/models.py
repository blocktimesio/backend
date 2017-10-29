from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.models import TimeStampedModel
from redactor.fields import RedactorField

USER_MODEL = get_user_model()


class Post(TimeStampedModel):
    class STATUSES:
        DRAFT = 'draft'
        IN_REVIEW = 'in_review'
        READY = 'ready'
        PUBLISHED = 'published'

        CHOICES = (
            (DRAFT, 'Draft'),
            (IN_REVIEW, 'In Review'),
            (READY, 'Ready'),
            (PUBLISHED, 'Published'),
        )

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(USER_MODEL)
    status = models.CharField(max_length=8, choices=STATUSES.CHOICES, default=STATUSES.DRAFT)
    tags = models.ManyToManyField('Tag', blank=True)
    content = RedactorField()

    pub_date = models.DateTimeField()

    class Meta:
        ordering = ['-pub_date']
        app_label = 'post'


class Tag(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        app_label = 'post'
