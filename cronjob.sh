#!/bin/bash
00 06 * * * cd /app && /usr/local/bin/python download_model.py >> /var/log/cron.log 2>&1