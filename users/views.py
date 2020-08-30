import logging
from django.db.models import Q
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from . serializers import BaseLoginRegisterRequestSerializer, TransactionListSerializer, UserCurrentMonthDetailsSerializer, RegisterFormSerializer
from wallet.models import Wallet, Transaction
from wallet_application.mixins import AuthRequiredMixin

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    def post(self, request):
        registerform = RegisterFormSerializer(data=request.POST)
        registerform.is_valid(raise_exception=True)
        if not User.objects.filter(username=registerform.data.get('phone_no')).exists():
            register_data = {
                'username': registerform.data.get('phone_no'),
                'first_name': registerform.data.get('first_name', ''),
                'last_name': registerform.data.get('last_name', ''),
                'email': registerform.data.get('email', ''),
                'is_active': True,
                'password': registerform.data.get('password')
            }
            try:
                user = User.objects.create_user(**register_data)
            except Exception as e:
                logger.error('Error while create user object')
                return Response({'success': False, 'msg': 'User not created due to system error'})
            Wallet.objects.create(user=user)
        else:
            return Response({'success': False, 'msg': 'User already exists'})
        return Response({'success': True, 'msg': 'User created successfully'})


class LoginView(APIView):
    def post(self, request):
        login_form = BaseLoginRegisterRequestSerializer(data=request.POST)
        login_form.is_valid(raise_exception=True)
        user = authenticate(username=login_form.data.get('phone_no'), password=login_form.data.get('password'))
        if user:
            token, created = Token.objects.get_or_create(user=user)
            try:
                Wallet.objects.get(user=user)
            except Wallet.DoesNotExist:
                Wallet.objects.create(user=user)
            return Response({'token': token.key, 'success': True})
        else:
            return Response({'success': False, 'error': 'Incorrect Username or Password'})


class TransactionsView(AuthRequiredMixin, APIView):

    def get(self, request):
        transaction_list = Transaction.objects.filter(Q(wallet=request.user.wallet) |
                                                      Q(credit_or_payer_wallet=request.user.wallet))
        if request.GET.get('page'):
            try:
                page = int(request.GET.get('page'))
            except ValueError:
                return Response({'success': False, 'msg': 'Invalid Page No'})
            page_size = 1
            transaction_list = transaction_list[page_size * (page - 1):page_size * page]
        serialized_list = TransactionListSerializer(instance=transaction_list, many=True, context={'user': request.user}).data
        return Response({'data': serialized_list})


class UserCurrentMonthView(AuthRequiredMixin, APIView):

    def get(self, request):
        serializer = UserCurrentMonthDetailsSerializer(request.user).data
        return Response({'data': serializer})
