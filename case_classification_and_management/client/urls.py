from django.urls import path

from .views import book_now, home

urlpatterns = [
    path("home", home, name="client_home"),
    path("booking/<int:id>", book_now, name="client_booking")
]