from django.core.management.base import BaseCommand, CommandError

import prisoners.models


class Command(BaseCommand):
    """
    Re-save every Prisoner in the database, in order to ensure cached fields
    are up to date.
    """

    def handle(self, *args, **options):
        for a in prisoners.models.PrisonerArrest.objects.all():

            print('pk = {}: {}'.format(a.pk, a.arrest_year))

            if not a.arrest_year:
                if a.arrest_month and not a.arrest_day:
                    raise CommandError(
                        'no year and month found ({})'
                        .format(a.arrest_month))
                if not a.arrest_month and a.arrest_day:
                    raise CommandError(
                        'no year and day found ({})'
                        .format(a.arrest_day))
                if a.arrest_month and a.arrest_day:
                    raise CommandError(
                        'no year and month ({}) and day ({}) found'
                        .format(a.arrest_month, a.arrest_day))

            else:
                d = '{0:04}'.format(a.arrest_year)
                if a.arrest_month:
                    d += '-{0:02}'.format(a.arrest_month)
                    if a.arrest_day:
                        d += '-{0:02}'.format(a.arrest_day)

                a.partial_date = d
                a.save()

                print('Saved {}'.format(a.partial_date))
