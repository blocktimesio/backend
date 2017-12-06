import logging
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.users.models import User as UserModel
from django_dynamic_fixture import G

User = get_user_model()  # type: UserModel


class BaseTest(APITestCase):
    PASSWORD = '123'
    csrf_checks = False

    def run(self, result=None):
        logger = logging.getLogger()
        graylog = logger.handlers[0]
        logger.removeHandler(graylog)

        super(BaseTest, self).run(result)

    # def setUp(self):
    #     self.user = G(User)
