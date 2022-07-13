from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from services.base_model import BaseModel


def product_directory_path(instance, filename):
    date_now = datetime.now()
    date = date_now.strftime("%d%m%Y_%H:%M:%S")

    return f"media/{instance.product_slug}_{date}_{filename}"


class ProductsModel(BaseModel):
    image = models.FileField(
        upload_to=product_directory_path,
        null=True,
        blank=True,
        verbose_name=_("Product Image"),
    )

    product_slug = models.SlugField(verbose_name=_("Product Slug"), unique=True)

    url = models.URLField(verbose_name=_("Product Url"))

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    @property
    def image_path(self):
        if self.image:
            return str(self.image)

    @property
    def sales_amount(self):
        return self.sales.count()

    @property
    def sales_dates(self):
        dates = [
            str(sale_date.insertion_date)
            for sale_date in self.sales.filter(is_active=True)
        ]
        return list(dict.fromkeys(dates))

    def get_sales_amount_on(self, date: datetime.date):
        return self.sales.filter(insertion_date=date).count()

    def __str__(self):
        return f"Product of id {self.id}"


class SalesModel(BaseModel):
    products = models.ForeignKey(
        ProductsModel,
        on_delete=models.CASCADE,
        verbose_name=_("Products"),
        related_name="sales",
        null=True,
        blank=True,
    )
    insertion_date = models.DateField(
        auto_now_add=True, verbose_name=_("Insertion Date")
    )

    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

    def __str__(self):
        return f"Sale of id {self.id}"
