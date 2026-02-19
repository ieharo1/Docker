"""
WSGI config for monitoring dashboard project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()


class StagingHostValidationMiddleware:
    """Middleware to bypass host validation in staging environment"""

    def __init__(self, app):
        self.app = app
        self.is_staging = os.environ.get("ENVIRONMENT") == "staging"

    def __call__(self, environ, start_response):
        if self.is_staging:
            # In staging, allow requests from any host
            # This is necessary for internal docker services to communicate
            environ["HTTP_HOST"] = "localhost"

        return self.app(environ, start_response)


# Wrap application with middleware in staging
if os.environ.get("ENVIRONMENT") == "staging":
    application = StagingHostValidationMiddleware(application)
