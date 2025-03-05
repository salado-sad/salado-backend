# from django.urls import path
# from .views import SignUpView, SignInView, UserProfileView, VerifyEmailView
#
# urlpatterns = [
#     path('signup/', SignUpView.as_view(), name='signup'),
#     path('signin/', SignInView.as_view(), name='signin'),
#     path('profile/', UserProfileView.as_view(), name='profile'),
#     path('verify/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify')
# ]
#
#
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, get_user_profile, CustomTokenObtainPairView, logout_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', get_user_profile, name='profile'),
    path('logout', logout_view, name='logout')
]
