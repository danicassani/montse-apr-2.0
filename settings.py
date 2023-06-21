import os
from dotenv import load_dotenv
load_dotenv() # load all the variables from the env file

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = "6few3nci_q_o@l1dlbk81%wcxe!*6r29yu629&d97!hiqat9fa"

DEFAULT_AUTO_FIELD='django.db.models.AutoField'



# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#     }
# }


"""
To connect to an existing postgres database, first:
pip install psycopg2
then overwrite the settings above with:
"""
name = os.getenv('POSTGRES_DB')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
hostname = os.getenv('POSTGRES_HOSTNAME')
port = os.getenv('POSTGRES_PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': name,
        'USER': user,
        'PASSWORD': password,
        'HOST': hostname,
        'PORT': port,
    }
}


INSTALLED_APPS = ("db",)
