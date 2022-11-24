from unicodedata import name
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView

from .views import SignupView,UserBookView,UpdateUserProfileView

app_name = 'accounts'

urlpatterns = [
    path('home/',UserBookView.as_view(),name='home'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('signup/',SignupView.as_view(),name='signup'),
    path('home/<int:pk>/update',UpdateUserProfileView.as_view(),name='update-user')

]