from django.urls import path
from .views import *


urlpatterns = [
	path('', navigation, name='navigation'),
	path('login-user/', LoginView, name='login-user'),
	path('logout-user/', LogoutView, name='logout-user'),
	path('change-password/', myPasswordChangeView.as_view(), name='change-password'),
	path('user-creation/', myCreateUserView, name='user-creation'), 
	path('create-profile/', createProfileView, name='create_profile'),
	path('edit-profile/', EditProfileView, name='edit_profile'),
	path('profile-detail/', profileDetailView, name='profile-detail'),	
]
