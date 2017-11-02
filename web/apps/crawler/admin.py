from django_mongoengine import mongo_admin as admin
from .models import CoindeskItems


@admin.register(CoindeskItems)
class CoindeskItemsAdmin(admin.DocumentAdmin):
    def log_change(self, request, object, message):
        pass

    def log_additional(self, request, object, message):
        pass
