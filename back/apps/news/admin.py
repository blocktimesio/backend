from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import RankConfig

admin.site.register(RankConfig, SingletonModelAdmin)
