from django.urls import path
from login_system import views as login_system_views

urlpatterns = [
    # path('login', login_system_views.login, name='login'),
    # path('logout', login_system_views.logout, name='logout'),
    path('signup', login_system_views.signup, name='signup'),
]
