from django.urls import path

from registration.api.views import RegisterView, LoginView, ResetChangePasswordView

urlpatterns = [
    path('registration/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    # path('logout/', LogoutView.as_view()),
    path('change_password/', ResetChangePasswordView.as_view())
]

