from django.contrib import admin

from .models import ProductsModel, SalesModel


@admin.register(SalesModel)
class SalesAdmin(admin.ModelAdmin):
    list_display = ("id", "insertion_date", "modification_date")


class SalesInline(admin.TabularInline):
    model = SalesModel
    verbose_name = "Sale"
    verbose_name_plural = "Sales"
    extra = 0
    fields = ("id", "is_active", "insertion_date", "modification_date")
    readonly_fields = ("insertion_date", "modification_date")


@admin.register(ProductsModel)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ("id", "url", "image", "insertion_date", "modification_date")
    readonly_fields = ("id", "insertion_date", "modification_date")
    inlines = (SalesInline,)
