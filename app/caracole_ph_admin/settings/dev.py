from .base import *
from .base import env

SECRET_KEY = env("DEV_SECRET_KEY")

ENVIRONMENT = "DEV"

INSTALLED_APPS += [
    "debug_toolbar"
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

CORS_URLS_REGEX = r"^/api/.*$"
CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_FRONTEND_ORIGINS = env("ALLOWED_DEV_FRONTEND_ORIGINS", default="")

if ALLOWED_FRONTEND_ORIGINS == "":
    ALLOWED_FRONTEND_ORIGINS = []
else:
    ALLOWED_FRONTEND_ORIGINS: list = ALLOWED_FRONTEND_ORIGINS.split(",")

ALLOWED_FRONTEND_ORIGINS.append("http://localhost:5173")
ALLOWED_FRONTEND_ORIGINS.append("http://localhost:3000")

ALLOWED_BACKEND_ORIGINS = env("ALLOWED_DEV_BACKEND_ORIGINS", default="")
if ALLOWED_BACKEND_ORIGINS == "":
    ALLOWED_BACKEND_ORIGINS = []
else:
    ALLOWED_BACKEND_ORIGINS: list = ALLOWED_BACKEND_ORIGINS.split(",")

ALLOWED_BACKEND_ORIGINS.append("http://localhost:8000")

CORS_ALLOWED_ORIGINS = ALLOWED_FRONTEND_ORIGINS + ALLOWED_BACKEND_ORIGINS
CSRF_TRUSTED_ORIGINS = ALLOWED_BACKEND_ORIGINS + ALLOWED_FRONTEND_ORIGINS

ALLOWED_DEV_APP_HOSTS = env("ALLOWED_DEV_APP_HOSTS", default="")
if ALLOWED_DEV_APP_HOSTS == "":
    ALLOWED_DEV_APP_HOSTS = []
else:
    ALLOWED_DEV_APP_HOSTS: list = ALLOWED_DEV_APP_HOSTS.split(",")

ALLOWED_DEV_APP_HOSTS.append("localhost")
ALLOWED_HOSTS = ALLOWED_DEV_APP_HOSTS

FRONTEND_URL = "http://localhost:5173"
DESIGN_CIRCLE_API_URL = "http://localhost:8001"  # For local testing

ORIGIN_HEADER = "dev.api.caracole"

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

# JWT Configuration
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}
