from django.urls import path
from mains import views as mains_views


urlpatterns = [
    path('', mains_views.home, name='home'),
    path('about', mains_views.about, name='about'),
    path('estimate', mains_views.estimate, name='estimate'),
]
