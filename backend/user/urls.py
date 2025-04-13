"""
URL mappings for the user app.
"""
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path

from user.views import CreateUserView, ManageUserView, LogoutView, TransactionView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('profile/', ManageUserView.as_view(), name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
]
