"""
Django settings for RentMatch project.

"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# SECURITY keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_-f^hypzb=1$ltp7l)^ul!g4%3j^=5d=&*za4q3!og$on0(+np'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []



# Add media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

REQUIRED_FIELDS = ['email']


# Application definition
AUTH_USER_MODEL = 'rentapp.User'

LOGIN_URL = 'login'  # The login URL name
LOGIN_REDIRECT_URL = '/'  # Redirect after successful login

LOGOUT_REDIRECT_URL = '/login/'  # Redirect after logout
LOGOUT_URL = 'logout'


ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_HTML = 'account/email_confirmation.html'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_REQUIRED = False

# Email settings for sending emails via Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mgimwaemily@gmail.com'  # Your Gmail email address
EMAIL_HOST_PASSWORD = 'xozm duca fgcn olbz'  # Your Gmail password


DEFAULT_FROM_EMAIL = 'mgimwaemily@gmail.com'  # Replace with your default email address


SESSION_COOKIE_SECURE = False  # Disable in development (HTTPS only)
CSRF_COOKIE_SECURE = False  # Disable in development (HTTPS only)




SESSION_COOKIE_SECURE = True  # Ensure cookies are only sent over HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookies
CSRF_COOKIE_SECURE = True  # Ensure CSRF cookies are only sent over HTTPS

SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Session expires when the browser is closed
SESSION_COOKIE_AGE = 900  # Session timeout in seconds (e.g., 30 minutes)


SITE_ID = 1


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'CLIENT_ID': '<your-client-id>',
        'SECRET': '<your-client-secret>',
        'SCOPE': [
            'profile',
            'email',
        ],
    },

    'apple': {
        'CLIENT_ID': '<your-client-id>',
        'SECRET': '<your-client-secret>',
        'TEAM_ID': '<your-team-id>',
        'KEY_ID': '<your-key-id>',
        'SCOPE': [
            'name',
            'email',
        ],
    }
}



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django_extensions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rentapp.apps.RentappConfig',
    'django.contrib.sites',  # Required for allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # For Google OAuth2
    'allauth.socialaccount.providers.apple',  # For Apple OAuth2

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'RentMatch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'RentMatch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
