from django.urls import path
from rest_framework.authtoken import views

from . import views as wallet_views

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('payment/', wallet_views.PaymentView.as_view(), name='payment_view'),
    path('get-balance/', wallet_views.BalanceView.as_view(), name='balance_view'),
]