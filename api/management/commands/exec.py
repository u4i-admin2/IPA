
import runpy
import sys

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not args:
            raise CommandError('must specify script args')
        sys.argv[:] = list(args)
        runpy.run_path(sys.argv[0], run_name='__main__')
