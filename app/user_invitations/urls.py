from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserInvitationViewSet
from .views import InvitedUserRegistrationView  # <- Import it separately

router = DefaultRouter()
router.register(r'invitations', UserInvitationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/<str:token>/', InvitedUserRegistrationView.as_view(), name='register-invited'),
]
