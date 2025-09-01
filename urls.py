from django.urls import path
from .views import login_user, logout_user, sign_up, update_profile

urlpatterns = [
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("signup/", sign_up, name="createuser"),
    path("update_password_user/", update_profile, name="account"),
]