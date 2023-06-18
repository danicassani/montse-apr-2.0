#!/usr/bin/env python
import os # default module
from dotenv import load_dotenv

def init_django():
    load_dotenv() # load all the variables from the env file
    name = os.getenv('POSTGRES_DB')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    hostname = os.getenv('POSTGRES_HOSTNAME')
    port = os.getenv('POSTGRES_PORT')
    import django
    from django.conf import settings

    if settings.configured:
        return



    settings.configure(
        INSTALLED_APPS=[
            'db',
        ],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': name,
                'USER': user,
                'PASSWORD': password,
                'HOST': hostname,
                'PORT': port,
            }
        },
        TIME_ZONE='Europe/Madrid',
    )
    django.setup()


if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    init_django()
    execute_from_command_line()