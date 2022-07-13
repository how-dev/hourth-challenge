from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Print Hello World"

    @staticmethod
    def add_arguments(parser):
        parser.add_argument("first_param", type=int)
        parser.add_argument("second_param", type=int)

    def handle(self, *_, **options):
        first = options["first_param"]
        second = options["second_param"]
        self.stdout.write(f"{first + second}")
