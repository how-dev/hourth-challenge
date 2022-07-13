from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    insertion_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Insertion Date")
    )
    modification_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Modification Date")
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
