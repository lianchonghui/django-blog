from .common import *

SECRET_KEY = os.environ.get('DJANGO_BLOG_SECRET_KEY')

ALLOWED_HOSTS = ['lianch.com','www.lianch.com','blog.lianch.com']
DEBUG = False

# django anymail
# use sendgrid
ANYMAIL = {
    "SENDGRID_API_KEY": os.environ.get('DJANGO_BLOG_SENDGRID_API_KEY'),
}
#EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
#DEFAULT_FROM_EMAIL = "练崇辉的博客 <blog@lianch.com>"

# use aliyun email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_USE_TLS = False
#EMAIL_PORT = 25
EMAIL_USE_SSL = True 
EMAIL_PORT = 465
EMAIL_HOST = 'smtp.lianch.com'
EMAIL_HOST_USER = 'blog@lianch.com'
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_BLOG_PASSWD')
DEFAULT_FROM_EMAIL = "练崇辉的博客 <blog@lianch.com>"

# use qq email
#EMAIL_USE_SSL = True
#EMAIL_HOST = "smtp.qq.com"
#EMAIL_PORT = 465
#EMAIL_HOST_USER = "865501908@qq.com"
#EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_BLOG_PASSWD')
#DEFAULT_FROM_EMAIL = "865501908@qq.com"
#DEFAULT_FROM_EMAIL = "练崇辉的博客 <865501908@qq.com>"