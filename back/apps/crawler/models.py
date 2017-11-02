from django_mongoengine import (Document, fields)


class CoindeskItems(Document):
    url = fields.URLField(max_length=512)
    slug = fields.StringField(max_length=256)

    title = fields.StringField(max_length=256)
    author = fields.StringField()
    text = fields.StringField()
    tags = fields.StringField()
    pub_date = fields.DateTimeField()

    image_url = fields.StringField(max_length=256)
    image_file_path = fields.StringField(max_length=256)

