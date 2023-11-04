from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register_view, name='register'),
    path('api/authenticate/', views.AuthenticationView.as_view(), name='authenticate'),
]