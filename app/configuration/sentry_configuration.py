import sentry_sdk
from os import environ as env

from ..util import app_mode, logger


_LOG_SENTRY_ENABLED = env.get("LOG_SENTRY_ENABLED", "False").lower() == "true"
_LOG_SENTRY_DSN = env.get("LOG_SENTRY_DSN")
_APP_VERSION = env.get("APP_VERSION")

if not _APP_VERSION:
    raise ValueError("APP_VERSION environment variable not set")


def configure_sentry():
    if not app_mode.is_prod():
        logger.debug(
            "Sentry info",
            extra={
                "Sentry Enabled": _LOG_SENTRY_ENABLED,
                "Sentry DSN": _LOG_SENTRY_DSN,
                "App Version": _APP_VERSION,
            },
        )

    if _LOG_SENTRY_ENABLED and _LOG_SENTRY_DSN:
        sentry_sdk.init(
            dsn=_LOG_SENTRY_DSN,
            environment=app_mode.get(),
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production,
            traces_sample_rate=1.0,
        )
