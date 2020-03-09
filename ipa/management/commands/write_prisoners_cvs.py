# coding: utf-8

import logging
import codecs
import os
import errno

import boto3

from django.conf import settings
from django.core.management.base import BaseCommand

from ipa.models import CsvState
from prisoners.models import Prisoner
from prisoners.renderers import PrisonerCsvRenderer

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    u"""
    The script takes care of updating the CSV file for prisoners on the
    S3 system. It will check the CsvState in ipa.models and based on that
    runs the csv generation or not.

    If the --force argument is passed to the command, the generation
    will run even if it hasn’t been requested by the app code. This may
    be useful for running on deploy.
    """

    help = u'Write CVS file for prisoners to S3'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true'
        )

    def write_to_s3(self, content):
        s3_res = boto3.resource(
            's3',
            region_name=settings.AWS_S3_REGION_NAME,
            config=boto3.session.Config(signature_version='s3v4'),
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

        s3_res.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
            StorageClass='REDUCED_REDUNDANCY',
            Key=settings.PRISONERS_CSV_FILE_KEY_NAME,
            Body=content)

    def write_to_file(self, content):
        filename = '{}/{}'.format(settings.MEDIA_ROOT, settings.PRISONERS_CSV_FILE_KEY_NAME)
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:
                if exc.errorno != errno.EEXIST:
                    self.stderr.write('Error openning file (error={}'.format(str(exc)))
                    return

        with codecs.open(filename, 'w', encoding='utf8') as csvfile:
            csvfile.write(content.read().decode('utf-8'))
            csvfile.close()

    def handle(self, *args, **options):

        csv_state = CsvState.objects.first()
        if csv_state is None:
            csv_state = CsvState.objects.create(
                should_write_csv=True)

        if (options['force'] is False and
                csv_state.should_write_csv is False):
            self.stdout.write(u'CSV file is updated')
            return

        renderer = PrisonerCsvRenderer()
        qs = Prisoner.objects.all()
        count = qs.count()
        self.stdout.write('Writing {} prisoner records to CSV file'.format(count))
        content = renderer.render(qs)
        content.seek(0)

        if(settings.AWS_ACCESS_KEY_ID is None or
                settings.AWS_SECRET_ACCESS_KEY is None or
                settings.AWS_STORAGE_BUCKET_NAME is None):
            self.write_to_file(content)
        else:
            self.write_to_s3(content)

        csv_state.should_write_csv = False
        csv_state.save()
