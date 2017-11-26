import os
import logging
import requests
import socialshares
from django.conf import settings
from django.core.files import File
from django.contrib.postgres.fields import JSONField
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from datetime import datetime
from django.template.defaultfilters import (
    striptags, truncatewords, truncatechars
)
from solo.models import SingletonModel

logger_crawlers = logging.getLogger('crawlers')


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

        if self.domain.coef:
            rank *= float(self.domain.coef)

        return rank

    @property
    def short_text(self):
        return truncatewords(striptags(self.text), 30)

    def update_social_data(self) -> None:
        if not self.url_raw:
            message = 'News ID={} has not url_raw field'.format(self.id)
            logger_crawlers.warning(message)
            return

        social_data = {}
        try:
            social_data = socialshares.fetch(
                self.url_raw,
                ['pinterest', 'linkedin', 'google', 'reddit']
            )
            fb_data = self._get_fb_data(self.url_raw)
            social_data.update(fb_data)
        except Exception as e:
            message = 'Error at fetch social shares for {}'.format(self.url_raw)
            logger_crawlers.error(message, exc_info=True)

        self.social = social_data
        try:
            self.save()
        except Exception as e:
            message = 'Error at saving News ID={} at updating social data'.format(self.id)
            logger_crawlers.error(message)

    def _get_fb_data(self, url: str) -> dict:
        if not self.url_raw:
            message = 'News ID={} has not url_raw field'.format(self.id)
            logger_crawlers.warning(message)
            return {}

        fb_url = 'https://graph.facebook.com/?key={}&id={}'.format(
            os.environ.get('FB_KEY', ''),
            url
        )
        fb_response = requests.get(fb_url)
        if fb_response.status_code == 200:
            fb_data = fb_response.json()
            share_data = fb_data.get('share', {})
            return {'facebook': share_data}
        else:
            message = 'Error at get Facebook shares for {}'.format(self.url_raw)
            logger_crawlers.error(message, exc_info=True)
            return {}

    def load_image(self) -> None:
        if not self.image_url:
            message = 'News ID={} has not field image_url'
            logger_crawlers.warning(message)
            return

        try:
            res = requests.get(self.image_url)
            if res.status_code == requests.codes.ok:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(res.content)
                img_temp.flush()

                image_path = 'news_images/{}/{}'.format(
                    self.domain.name,
                    os.path.basename(self.image_url)
                )
                self.image.save(image_path, File(img_temp), save=True)
        except Exception as e:
            message = 'Error at saving image for News ID={}'.format(self.id)
            logger_crawlers.error(message, exc_info=True)

        try:
            self.save()
        except Exception as e:
            logger_crawlers.error('Error at create News', exc_info=True)

    def add_tags(self, tags_names: list) -> None:
        tags = []
        for name in tags_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tags.append(tag)

        for tag in tags:
            self.tags.add(tag)

    def __str__(self):
        return truncatechars(self.title, 32)

    class Meta:
        app_label = 'news'
