"""Celery application bootstrap."""

import os

from celery import Celery
from celery.schedules import crontab

from accounts.core.config import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rakshak_backend.settings")

app = Celery("rakshak_backend")
app.conf.broker_url = settings.celery_broker_url
app.conf.result_backend = settings.celery_result_backend
app.conf.timezone = "Asia/Kolkata"
app.conf.broker_connection_retry_on_startup = True
app.conf.task_track_started = True
app.conf.beat_schedule = {
    "poll-triggers-every-15-minutes": {
        "task": "triggers.poll_external_sources",
        "schedule": crontab(minute="*/15"),
    },
    "create-nightly-claims": {
        "task": "claims.create_nightly_claims",
        "schedule": crontab(minute=50, hour=23),
    },
}

if os.name == "nt":
    # Celery prefork is unstable on Windows; solo keeps local scheduled jobs reliable.
    app.conf.worker_pool = "solo"
    app.conf.worker_concurrency = 1

app.autodiscover_tasks(["triggers", "claims"])
