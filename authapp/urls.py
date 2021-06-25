from django.urls import path

from authapp.views import login, RegisterCreateView, logout, profile, verify

app_name = 'authapp'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', RegisterCreateView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<email>/<key>/', verify, name='verify'),
]
