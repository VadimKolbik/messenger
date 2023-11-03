from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('people/', PeopleView.as_view(), name='people'),
]