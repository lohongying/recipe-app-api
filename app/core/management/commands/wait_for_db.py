import time
from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        """ Entrypoint for command"""
        self.stdout.write(
            "Waiting for database...")
        # standard output for logging things to the console
        db_up = False  # tract db status
        while db_up is False:
            try:
                # determine if the database is ready
                self.check(databases=['default'])
                db_up = True

            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second ...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available'))
