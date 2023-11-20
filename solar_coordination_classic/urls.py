from django.urls import path

from . import views

urlpatterns = [
    path('participants', views.participants_view, name='participants-view'),

    path('', views.welcome_page, name='welcome'),

    path("task", views.index, name="main"),
    path("overview", views.overview, name="overview"),
]