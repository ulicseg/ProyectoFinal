from .settings import *

# Sobrescribe cualquier configuración específica aquí
DEBUG = True

# Puedes agregar configuraciones adicionales específicas para tu entorno local

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
           'NAME': 'base_proyecto',
           'USER': 'root',
           'PASSWORD': 'root',
           'HOST': 'localhost', 
           'PORT': '3306',       
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(BASE_DIR),'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(os.path.dirname(BASE_DIR),'static'),)


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR),'media')