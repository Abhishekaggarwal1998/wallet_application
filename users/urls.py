from django.urls import path
from rest_framework.authtoken import views

from . import views as user_views

urlpatterns = [
    path('register/', user_views.RegisterView.as_view(), name='register_view'),
    path('login/', user_views.LoginView.as_view(), name='login_view'),
    path('transactions-list/', user_views.TransactionsView.as_view(), name='transactions-list'),
    path('get-month-summary/', user_views.UserCurrentMonthView.as_view(), name='month-summary')
]