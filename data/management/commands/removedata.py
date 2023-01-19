import hashlib
from django.core.management.base import BaseCommand
import pandas as pd

from data.models import Report


class Command(BaseCommand):
    help = 'Delete all data.'

    def handle(self, *args, **kwargs):
        Report.objects.all().delete()
