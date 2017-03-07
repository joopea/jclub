from time import sleep

from fabric.api import env, run
from fabric.context_managers import settings
from fabric.contrib.files import exists

from deployscript import utils
from deployscript.services import Service, ManagedService, Gunicorn


class GunicornAdmin(Gunicorn):
    env_local = {
        'wsgi_config': '{release_config_path}gunicorn_admin.conf.py',
        'wsgi_socket': '{local_path}run/wsgi_admin.sock',
        'wsgi_pid': '{local_path}run/wsgi_admin.pid',
        'wsgi_log': '{local_path}log/wsgi_admin.log',
        'wsgi_command': '{release_path}env/bin/gunicorn_django',
        'wsgi_process_name': '{project_env}_wsgi_admin',
        'wsgi_workers': 2,
        'wsgi_max_requests': 1000,
    }

    env_defaults = {
        'wsgi_socket_admin': '{local_path}run/wsgi_admin.sock',
    }

    def processmanager_conf(self):
        if env.host not in env.wsgi_hosts:
            return None

        return {
            'environment': {
                            'DJANGO_SETTINGS_MODULE': 'settings.locals_admin'
                            },
            'name': str('{wsgi_process_name}'),
            'cmd': str('{release_path}/env/bin/gunicorn -c {wsgi_config} wsgi:application'),
            'cwd': '{release_path}source/',
            'user': 'root',
        }
