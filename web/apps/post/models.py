from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import truncatechars
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
    author = models.ForeignKey(USER_MODEL, related_name='author')
    assigned = models.ForeignKey(USER_MODEL, related_name='assigned', blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUSES.CHOICES, default=STATUSES.DRAFT)
    tags = models.ManyToManyField('Tag', blank=True)
    content = RedactorField()

    pub_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return truncatechars(self.name, 32)

    class Meta:
        ordering = ['-pub_date']
        app_label = 'post'


class Tag(TimeStampedModel):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    author = models.ForeignKey(USER_MODEL)

    def __str__(self):
        return truncatechars(self.name, 32)

    class Meta:
        app_label = 'post'
