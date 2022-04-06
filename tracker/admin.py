from django.apps import apps
from django.contrib import admin

app1 = apps.get_app_config("tracker")

for model_name, model in app1.models.items():
    admin.site.register(model)

app2 = apps.get_app_config("users")

for model_name, model in app2.models.items():
    admin.site.register(model)
