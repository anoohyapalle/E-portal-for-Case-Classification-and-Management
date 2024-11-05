from django.urls import path

from .views import home, done_booking, remove_case_type

urlpatterns = [
    path("home", home, name="lawyer_home"),
    path("done_booking/<int:id>", done_booking, name="lawyer_done_booking"),
    path("remove_case_type/<int:id>", remove_case_type, name="remove_case_type"),
]