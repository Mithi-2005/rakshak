"""Celery tasks for trigger polling."""

import logging

from accounts.db.session import get_db_session
from rakshak_backend.celery import app
from triggers.services.event_service import poll_all_active_zones

logger = logging.getLogger(__name__)


@app.task(name="triggers.poll_external_sources")
def poll_external_sources() -> dict[str, int]:
    with get_db_session() as db:
        result = poll_all_active_zones(db)
    logger.info("Trigger polling task complete | result=%s", result)
    return result

