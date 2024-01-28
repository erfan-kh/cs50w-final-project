"""serverV1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
"""

# Import required modules
from django.urls import path
from . import views

# Define URL patterns
urlpatterns = [
    # Map the root URL to the index view
    path('', views.index, name='index'),

    # Map the login URL to the login view
    path("login", views.login_view, name="login"),

    # Map the logout URL to the logout view
    path("logout", views.logout_view, name="logout"),

    # Map the register URL to the register view
    path("register", views.register, name="register"),

    # Map the Turn_on URL to the Turn_on view
    path('Turn_on/', views.Turn_on, name='on'),

    # Map the Turn_off URL to the Turn_off view
    path('Turn_off/', views.Turn_off, name='off'),

    # Map the send_value URL to the send_value view
    path('send_value/', views.send_value, name='send_value'),

    # Map the sensor URL to the sensor view
    path('sensor/', views.sensor, name='sensor'),

    # Map the chart URL to the chart view, with a user_id parameter
    path('chart/<int:user_id>', views.chart, name='chart'),

    # Map the profile URL to the profile view, with a user_id parameter
    path("profile/<int:user_id>", views.profile, name="profile"),

]
