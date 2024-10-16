from django.urls import path
from . import views

urlpatterns = [
    path('create', views.sign_up, name="sign_up"),
]
