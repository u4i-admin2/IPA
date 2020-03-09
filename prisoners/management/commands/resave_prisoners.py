from django.core.management.base import BaseCommand

import prisoners.models


class Command(BaseCommand):
    """
    Re-save every Prisoner in the database, in order to ensure cached fields
    are up to date.
    """

    def handle(self, *args, **options):
        for prisoner in prisoners.models.Prisoner.objects.all():
            print('Saving: %r' % (prisoner,))
            prisoner.save()
