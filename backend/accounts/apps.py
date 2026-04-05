"""Accounts app configuration"""

import sys

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "accounts"

    def ready(self) -> None:
        skipped_commands = {
            "makemigrations",
            "migrate",
            "collectstatic",
            "check",
            "shell",
            "createsuperuser",
            "test",
        }
        if len(sys.argv) > 1 and sys.argv[1] in skipped_commands:
            return

        from accounts.db.session import init_db

        init_db()
