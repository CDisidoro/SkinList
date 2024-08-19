#!/bin/bash
set -a
. /app/.env
set +a
/usr/local/bin/python /app/manage.py update_cosmetics
/usr/local/bin/python /app/manage.py fetch_shop