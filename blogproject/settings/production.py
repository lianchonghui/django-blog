from .common import *

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['.zmrenwu.com']
DEBUG = False

# django anymail
ANYMAIL = {
    "SENDGRID_API_KEY": os.environ.get('DJANGO_SENDGRID_API_KEY'),
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = "zmrenwu_blog@zmrenwu.com"
