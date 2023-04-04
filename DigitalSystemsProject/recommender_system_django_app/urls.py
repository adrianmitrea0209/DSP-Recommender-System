from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="Homepage"),
    path('login/', views.login_function, name='Login'),
    path('logout/', views.logout_function, name='Logout'),
    path('register/', views.register_function, name='Register'),
]