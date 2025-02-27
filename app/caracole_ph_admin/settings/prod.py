from .base import *
from datetime import timedelta

ENVIRONMENT = "PROD"
SECRET_KEY = env("PROD_SECRET_KEY")

# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# X_FRAME_OPTIONS = "DENY"

ALLOWED_FRONTEND_ORIGINS = env("ALLOWED_PROD_FRONTEND_ORIGINS", default="")

if ALLOWED_FRONTEND_ORIGINS == "":
    ALLOWED_FRONTEND_ORIGINS = []
else:
    ALLOWED_FRONTEND_ORIGINS: list = ALLOWED_FRONTEND_ORIGINS.split(",")

ALLOWED_BACKEND_ORIGINS = env("ALLOWED_DEV_BACKEND_ORIGINS", default="")
if ALLOWED_BACKEND_ORIGINS == "":
    ALLOWED_BACKEND_ORIGINS = []
else:
    ALLOWED_BACKEND_ORIGINS: list = ALLOWED_BACKEND_ORIGINS.split(",")

CORS_ALLOWED_ORIGINS = ALLOWED_FRONTEND_ORIGINS + ALLOWED_BACKEND_ORIGINS
CSRF_TRUSTED_ORIGINS = ALLOWED_BACKEND_ORIGINS + ALLOWED_FRONTEND_ORIGINS

ALLOWED_APP_HOSTS = env("ALLOWED_PROD_APP_HOSTS", default="")
if ALLOWED_APP_HOSTS == "":
    ALLOWED_APP_HOSTS = []
else:
    ALLOWED_APP_HOSTS: list = ALLOWED_APP_HOSTS.split(",")

ALLOWED_HOSTS = ALLOWED_APP_HOSTS


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
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

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ("rest_framework.renderers.JSONRenderer",)
