from django.urls import path

from . import views

urlpatterns = [
    path('participants', views.participants_view, name='participants-view'),

    path('', views.welcome_page, name='welcome'),

    path("task", views.index, name="main"),
    path("overview", views.overview, name="overview"),
    path("fetch_solar_and_booked_values", views.fetch_solar_and_booked_values, name="fetch_solar_and_booked_values"),
    path('create_booking/', views.create_booking, name='create_booking'),

]