from .common import *

SECRET_KEY = os.environ.get('DJANGO_BLOG_SECRET_KEY')

ALLOWED_HOSTS = ['blog.lianch.com']
DEBUG = False

# django anymail
ANYMAIL = {
    "SENDGRID_API_KEY": os.environ.get('DJANGO_BLOG_SENDGRID_API_KEY'),
}
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
DEFAULT_FROM_EMAIL = "lianchonghui@foxmail.com"
