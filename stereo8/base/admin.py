from django.contrib import admin
from django.apps import apps

base_app = apps.get_app_config('base')
for model in base_app.models.values():
    admin.site.register(model)
