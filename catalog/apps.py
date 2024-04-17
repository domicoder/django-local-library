# pylint: disable=unused-import
# pylint: disable=missing-module-docstring
from django.apps import AppConfig


class CatalogConfig(AppConfig):
    """Class representing a catalog"""

    # set the type of the primary key to a BigAutoField
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
