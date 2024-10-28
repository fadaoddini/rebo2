import os
SECRET_KEY = 'django-insecure-)l7^&$3*+x=-g7b^job8*d(qz98g3b5ahv2!lk*5amuk+7bi#n'
DEBUG = True
ALLOWED_HOSTS = ['*']
ZARRINPAL_MERCHANT_ID = 'e701a7c2-73ae-11e8-b07d-005056a205be'
DB_NAME = 'rebo'
DB_USER = 'rebo'
DB_PASS = 'rebo'
DB_HOST = 'localhost'
DB_PORT = 5432
API_MAX_SMS = 'oUSMoSz9YIujHc-XyaanUMimxpSq8rpbx3KHS1nMumA='
API_NESHAN = 'service.ad5200afd6b144a3a99f364d1f407016'
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000']

ADDRESS_SERVER = 'http://localhost:3000'
BACKEND_URL = 'http://localhost:8000'
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",

]


# import os
# DEBUG = False
# ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'rebo.ir', 'iscode.ir']
# SECRET_KEY = os.environ.get("SECRET_KEY")
# DB_NAME = os.environ.get("DB_NAME")
# DB_USER = os.environ.get("DB_USER")
# DB_PASS = os.environ.get("DB_PASS")
# DB_HOST = os.environ.get("DB_HOST")
# DB_PORT = os.environ.get("DB_PORT")
# API_MAX_SMS = os.environ.get("API_MAX_SMS")
# API_NESHAN = os.environ.get("API_NESHAN")
# ZARRINPAL_MERCHANT_ID = os.environ.get("ZARRINPAL_MERCHANT_ID")
# SECURE_SSL_REDIRECT = False
# SESSION_COOKIE_NAME = 'sessionid'
# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
# CSRF_TRUSTED_ORIGINS = ['https://rebo.ir', 'https://iscode.ir']
# ADDRESS_SERVER = 'https://iscode.ir'
# BACKEND_URL = 'https://rebo.ir'
#
# CORS_ALLOWED_ORIGINS = [
#      "https://iscode.ir",
#      "https://rebo.ir",
# ]
