from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *


app_name = 'users'

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('people/', PeopleView.as_view(), name='people'),
    path('add-to-friends/<int:friend_id>/', add_to_friends, name='add_to_friends'),
    path('friends/', FriendsView.as_view(), name='friends'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', UserPasswordChangeDoneView.as_view(), name='password_change_done'),
]