from django.core.management.base import BaseCommand
from prisoners.renderers import PrisonerCsvRenderer
import prisoners.models as prisoners_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        queryset = prisoners_models.Prisoner.prefetch_queryset(
            prisoners_models.Prisoner.objects.all())
        renderer = PrisonerCsvRenderer()
        renderer.render(queryset)

        print('Done')
