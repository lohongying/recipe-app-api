"""
Test custom django management commands.
"""

# mock behavior of the database (simulate the database response)
from unittest.mock import patch

# possible error when we try to connect ot the database
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
# call the command we are testing
from django.db.utils import OperationalError  # an option of error we may get
from django.test import SimpleTestCase  # do not need migration


# Command.check is provided by BaseCommand class
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    # order matters as it applies the argument inside-out
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting OperationalError"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        # simulating how the error comes through
        # the first 2 times, we call the mock method, raise the psycopg2error,
        # the next 3 times, we raise the operational error
        # the 6th time we call it, returns a True
        call_command('wait_for_db')
        # check the number of timese we call the patched_check method
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
