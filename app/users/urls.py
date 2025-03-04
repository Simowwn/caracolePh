from django.urls import path
from . import views

urlpatterns = [
    # Add your user-related URL patterns here
    # The LoginView is already included in the main urls.py file at 'api/login/'
    # If you need to add more user-related endpoints, add them below
    # For example:
    # path('me/', views.UserProfileView.as_view(), name='user-profile'),
    # List all users
    path('', views.UserListView.as_view(), name='user-list'),
    path('<uuid:user_id>/', views.UserUpdateView.as_view(), name='user-update'),
]
