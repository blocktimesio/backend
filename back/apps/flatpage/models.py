from django.db import models
from django.template.defaultfilters import truncatechars


class Flatpage(models.Model):
    slug = models.SlugField(max_length=128, unique=True)
    title = models.CharField(max_length=128)
    content = models.TextField()
    is_show = models.BooleanField(default=True)

    def __str__(self):
        return truncatechars(self.title, 32)