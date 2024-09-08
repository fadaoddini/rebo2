"""
Django settings for rebo project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from pathlib import Path

from django.contrib.messages import constants as messages

from rebo.local_setting import *

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.INFO: 'success',
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'catalogue.apps.CatalogueConfig',
    'transaction.apps.TransactionConfig',
    'company.apps.CompanyConfig',
    'index.apps.IndexConfig',
    'login.apps.LoginConfig',
    'info.apps.InfoConfig',
    'order.apps.OrderConfig',
    'chat.apps.ChatConfig',
    'learn.apps.LearnConfig',
    'law.apps.LawConfig',
    'shop.apps.ShopConfig',
    'transport.apps.TransportConfig',
    'cart.apps.CartConfig',
    'bid.apps.BidConfig',
    'divar.apps.DivarConfig',
    'hoghoogh.apps.HoghooghConfig',
    'widget_tweaks',
    'jalali_date',
    'rest_framework',
    'rest_framework_simplejwt',
    'qr_code',
    'django.contrib.humanize',
    'corsheaders',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://iscode.ir",
    "https://rebo.ir",
    "http://iscode.ir",
    "http://rebo.ir",
]

# اینو یادم باشه بعدا حذف کنم
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'rebo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
                'cart.context_processors.location_cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'rebo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST,
        'USER': DB_USER,
        'PORT': DB_PORT,
    }
}

ZARRINPAL = {
    'gateway_request_url': 'https://www.zarinpal.com/pg/services/WebGate/wsdl',
    'gateway_callback_url': 'http://localhost:3000/payment/verify/',  # تغییر به آدرس محلی
    'merchant_id': ZARRINPAL_MERCHANT_ID
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

# default settings (optional)
JALALI_DATE_DEFAULTS = {
    'Strftime': {
        'date': '%y/%m/%d',
        'datetime': '%H:%M:%S _ %y/%m/%d',
    },
    'Static': {
        'js': [
            # loading datepicker
            'admin/js/django_jalali.min.js',
            # OR
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.core.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/calendar.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc-fa.js',
            # 'admin/js/main.js',
        ],
        'css': {
            'all': [
                'admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css',
            ]
        }
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login-mobile'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000000
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'login.mybackend.MobileBackend'
]
AUTH_USER_MODEL = 'login.MyUser'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ) if DEBUG else (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

CART_SESSION_ID = 'cart'
ADDRESS_SHIPPING = 'location'

ADDRESS_SERVER = 'https://localhost:3000'
