from django.contrib import admin

from hotel.models import Hotel

from django.contrib import admin
from django.apps import apps

# Dynamically register all models
app = apps.get_app_config("hotel")

for model in app.get_models():
    # Check if the model is already registered to avoid double registration
    if not admin.site.is_registered(model):
        # Automatically register model with all fields displayed
        class AutoAdmin(admin.ModelAdmin):

            list_display = [field.name for field in model._meta.fields]
            list_filter = [field.name for field in model._meta.fields if
                           field.get_internal_type() in (
                           "BooleanField", "CharField", "IntegerField")]
            search_fields = [field.name for field in model._meta.fields if
                             field.get_internal_type() in ("CharField", "TextField")]


        admin.site.register(model, AutoAdmin)