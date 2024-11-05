from django.contrib import admin
from django.urls import path, include
from .views import home, login, logout_default, register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('login', login, name="login"),
    path('register', register, name="register"),
    path('logout', logout_default, name="logout"),
    path('lawyer/', include("lawyer.urls")),
    path('client/', include("client.urls")),
]
