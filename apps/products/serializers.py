from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import ProductsModel, SalesModel


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesModel
        fields = ("id", "insertion_date")


class ProductsSerializer(serializers.ModelSerializer):
    sales = SalesSerializer(many=True)

    class Meta:
        model = ProductsModel
        fields = ("id", "image", "url", "insertion_date", "sales")

    @staticmethod
    def validate_date_format(date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValidationError(
                {"detail": "Incorrect data format, should be YYYY-MM-DD"}
            )

    def increment_representation(self, instance, representation):
        consult_date = self.context["consult_date"]

        if consult_date is not None:
            self.validate_date_format(consult_date)
            representation.update(
                {
                    "consult_date": consult_date,
                    "sales_on_the_day": instance.get_sales_amount_on(consult_date),
                }
            )
        else:
            sales_dates = instance.sales_dates
            representation.update(
                {
                    "sales": [
                        {
                            sale_date: instance.sales.filter(
                                insertion_date=sale_date
                            ).count()
                        }
                        for sale_date in sales_dates
                    ]
                }
            )

    def to_representation(self, instance):
        representation = {
            "id": instance.id,
            "product_url__image": instance.image_path,
            "product_url": instance.url,
            "product_url__created_at": str(instance.insertion_date),
        }

        self.increment_representation(instance, representation)

        return representation
