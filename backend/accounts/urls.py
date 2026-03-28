"""URLs for authentication"""

from django.urls import path
from .views import signup, login_view, logout_view, get_user

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('user/', get_user, name='get_user'),
]
