
from .common import *
import sentry_sdk

# Email
domain = os.getenv("Domain")
PASSWORD_ACTIVE_BASE_URL = domain +"accounts/api/v1/activate/jwt/"
PASSWORD_RESET_BASE_URL= domain +"accounts/api/v1/reset/pass/"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp4dev"
EMAIL_PORT = "25"
EMAIL_USE_TLS = False

EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""



# this config for sentry execute
sentry_sdk.init(
    dsn="https://1e69ea4a053483b336be0f2d7b144ea3@o4507802990870528.ingest.de.sentry.io/4507802992705616",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

