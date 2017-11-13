import os
import logging
from urllib.request import urlretrieve

import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from ..models import (Tag, Domain, News)

logger = logging.getLogger('crawlers')


class DjangoPipeline(object):
    def process_item(self, item, spider):
        tags_names = item.pop('tags', [])
        tags = []
        for name in tags_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tags.append(tag)

        domain_name = item.pop('domain')
        domain, created = Domain.objects.get_or_create(name=domain_name)

        is_exists = News.objects.filter(url=item['url']).exists()
        if is_exists:
            try:
                News.objects.filter(url=item['url']).update(**dict(item))
            except Exception as e:
                logger.error('Error at update News', exc_info=True)
        else:
            obj = News.objects.create(domain=domain, **item)
            for tag in tags:
                obj.tags.add(tag)

            image_url = item.get('image_url')
            if image_url:
                try:
                    res = requests.get(image_url)
                    if res.status_code == requests.codes.ok:
                        img_temp = NamedTemporaryFile(delete=True)
                        img_temp.write(res.content)
                        img_temp.flush()

                        image_path = 'news_images/{}/{}'.format(
                            obj.domain.name,
                            os.path.basename(image_url)
                        )
                        obj.image.save(image_path, File(img_temp), save=True)
                except Exception as e:
                    logger.error('Error at save image for news', exc_info=True)

            try:
                obj.save()
            except Exception as e:
                logger.error('Error at create new News', exc_info=True)