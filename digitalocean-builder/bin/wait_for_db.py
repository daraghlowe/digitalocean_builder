#!/usr/bin/env python3

import os.path
import sys
import time
from django.db import connections, OperationalError

sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))


def test_db_connection(max_retries: int = 8, delay_in_seconds: int = 5):
    conn = connections['default']

    for i in range(1, max_retries):
        print('Attempt number: {}'.format(i))

        try:
            conn.ensure_connection()
            if conn.is_usable():
                print('Database ready!')
                return
        except OperationalError:
            pass

        time.sleep(delay_in_seconds)

    raise RuntimeError('Database never became available!')


if __name__ == '__main__':
    print('Waiting for database to be available...')
    test_db_connection()
