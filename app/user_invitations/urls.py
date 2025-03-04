from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserInvitationViewSet

router = DefaultRouter()
router.register(r'invitations', UserInvitationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]