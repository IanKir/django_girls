from django.urls import path
from register.views import signup_view


urlpatterns = [
    path('signup/', signup_view, name="signup")
]
