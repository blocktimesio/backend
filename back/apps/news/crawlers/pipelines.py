import logging
from ..models import (Domain, News)

logger = logging.getLogger('crawlers')


class DjangoPipeline(object):
    def process_item(self, item, spider):
        tags_names = item.pop('tags', [])

        domain_name = item.pop('domain')
        domain, created = Domain.objects.get_or_create(name=domain_name)

        is_exists = News.objects.filter(url=item['url']).exists()
        if is_exists:
            try:
                News.objects.filter(url=item['url']).update(
                    views=item['views'],
                    comments=item['comments'],
                )
            except Exception as e:
                logger.error('Error at update News', exc_info=True)
        else:
            obj = News.objects.create(domain=domain, social={}, **item)

            obj.load_image()
            obj.add_tags(tags_names)
