from django.utils import timezone
from mongoengine import Document, fields


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

    created = fields.DateTimeField(default=timezone.now, null=True, required=False)
    updated = fields.DateTimeField(default=timezone.now, null=True, required=False)
