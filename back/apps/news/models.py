from django.db import models
from datetime import datetime
from django.utils import timezone
from mongoengine import (Document, fields)
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
        verbose_name = 'Rank formula config'


class News(Document):
    id = fields.StringField(required=True, primary_key=True)

    domain = fields.StringField(required=True)
    url = fields.StringField(required=True)
    slug = fields.StringField(required=True)
    title = fields.StringField(required=True)
    author = fields.StringField(required=True)
    text = fields.StringField(required=True)
    tags = fields.ListField(fields.StringField())
    pub_date = fields.StringField(required=True)

    social = fields.DictField(required=False, null=True)

    image_url = fields.StringField(required=False)
    image_file_path = fields.StringField(required=False)

    created = fields.DateTimeField(default=timezone.now)
    updated = fields.DateTimeField(default=timezone.now)

    @property
    def rank(self):
        if not self.social:
            return 0

        social = self.social  # type: dict

        fb_shares = 0
        fb_comments = 0
        fb_data = social.get('facebook', {})
        if fb_data:
            fb_shares = fb_data.get('share_count', 0)
            fb_comments = fb_data.get('comment_count', 0)

        reddit_ups = 0
        reddit_downs = 0
        reddit_data = social.get('reddit', {})
        if reddit_data:
            reddit_ups = reddit_data.get('ups')
            reddit_downs = reddit_data.get('downs')

        linkedin_shares = social.get('linkedin', 0)
        pinterest = social.get('pinterest', 0)

        config = RankConfig.get_solo()  # type: RankConfig

        rank = 0
        rank += fb_shares * config.fb_shares
        rank += linkedin_shares * config.linkedin_shares
        rank += reddit_ups * config.reddit_up
        # rank += fb_shares * 2
        # rank += views  * config.views
        # rank += comments * config.comments
        rank -= (datetime.now() - self.created).seconds / config.date_elapsed_seconds * config.date_coef
        return rank
