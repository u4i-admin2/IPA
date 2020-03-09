from django.core.management.base import BaseCommand

import prisoners.models as prisoners_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        prisoners_models.Prisoner.objects.all().update(is_published=True)
        print('Prisoner model updated')
