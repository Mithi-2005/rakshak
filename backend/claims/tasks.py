"""Celery tasks for claims processing."""

import logging

from accounts.db.session import get_db_session
from claims.services.claim_service import create_claims_for_unprocessed_triggers
from rakshak_backend.celery import app

logger = logging.getLogger(__name__)


@app.task(name="claims.create_nightly_claims")
def create_nightly_claims() -> dict[str, int]:
    with get_db_session() as db:
        created = create_claims_for_unprocessed_triggers(db)
    logger.info("Nightly claim generation complete | created=%s", created)
    return {"claims_created": created}
