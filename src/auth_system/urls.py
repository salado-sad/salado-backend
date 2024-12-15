from django.urls import path
from .views import SignUpView, SignInView, UserProfileView, VerifyEmailView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('verify/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify')
]
