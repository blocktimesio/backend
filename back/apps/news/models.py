from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from datetime import datetime
from django.template.defaultfilters import (
    striptags, truncatewords, truncatechars
)
from solo.models import SingletonModel


class RankConfig(SingletonModel):
    fb_shares = models.DecimalField(max_digits=9, decimal_places=5, default=2.)
    linkedin_shares = models.DecimalField(max_digits=9, decimal_places=5, default=1.5)
    reddit_up = models.DecimalField(max_digits=9, decimal_places=5, default=3.)
    twitter_shares = models.DecimalField(max_digits=9, decimal_places=5, default=1.1)
    views = models.DecimalField(max_digits=9, decimal_places=5, default=2.)
    comments = models.DecimalField(max_digits=9, decimal_places=5, default=5.)
    date_elapsed_seconds = models.PositiveIntegerField(default=3600)
    date_coef = models.DecimalField(max_digits=9, decimal_places=5, default=10)

    def __str__(self):
        return 'Rank formula config'

    class Meta:
        app_label = 'news'
        verbose_name = 'Rank formula config'


class Domain(models.Model):
    name = models.CharField(max_length=128)
    coef = models.DecimalField(max_digits=9, decimal_places=5, default=0.)

    def __str__(self):
        return '{} [{}]'.format(self.name, self.coef)

    class Meta:
        app_label = 'news'
        ordering = ['-name']


class Tag(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'news'
        ordering = ['-name']


class News(models.Model):
    domain = models.ForeignKey(Domain)
    url = models.URLField(unique=True)
    url_raw = models.URLField()
    slug = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    text = models.TextField(default='')
    tags = models.ManyToManyField(Tag, blank=True)
    pub_date = models.DateTimeField()

    social = JSONField(default=settings.DEFAULT_SOCIAL_NEWS)
    views = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)

    image = models.ImageField(blank=True, null=True, upload_to='news_images')
    image_url = models.URLField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def rank(self):
        if not self.social:
            return 0

        rank = 0
        social = self.social  # type: dict
        config = RankConfig.get_solo()  # type: RankConfig

        for f in config._meta.fields:
            value = float(getattr(config, f.name))
            setattr(config, f.name, value)

        fb_data = social.get('facebook', {})
        if fb_data:
            rank += config.fb_shares * fb_data.get('share_count', 0)

        reddit_data = social.get('reddit', {})
        if reddit_data:
            rank += config.reddit_up * reddit_data.get('ups', 0)

        rank += config.linkedin_shares * social.get('linkedin', 0)

        rank += self.views * config.views
        rank += self.comments * config.comments
        rank -= (datetime.now() - self.pub_date).seconds / float(config.date_elapsed_seconds * config.date_coef * 3600)
        return rank

    @property
    def short_text(self):
        return truncatewords(striptags(self.text), 30)

    def __str__(self):
        return truncatechars(self.title, 32)

    class Meta:
        app_label = 'news'
