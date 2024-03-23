# pylint: disable=unused-import
# pylint: disable=missing-module-docstring
from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
