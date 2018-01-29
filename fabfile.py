# coding:utf-8

from fabric.api import env,run
from fabric.operations import sudo

GIT_REPO = 'https://github.com/lianchonghui/django-blog.git'

env.user = 'lianch'

env.hosts = ['blog.lianch.com',]
env.port = '22'

def deploy():
    source_folder = '/home/lianch/sites/lianch.com/django-blog'
    sudo('systemctl stop gunicorn-blog.lianch.com')

    run('cd %s && git pull' % source_folder)
    run('cd {} && cp ./lensproject/settings/production.py ./lensproject/settings/__init__.py'.format(source_folder))
    run("""
        cd {} &&
        ../env/bin/pip install -r ./requirements/production.txt &&
        ../env/bin/python3 manage.py collectstatic --noinput &&
        ../env/bin/python3 manage.py migrate
        """.format(source_folder))
    sudo('systemctl start gunicorn-blog.lianch.com')
    #sudo('service nginx reload')
