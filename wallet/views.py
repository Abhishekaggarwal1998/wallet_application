import logging
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Wallet, Transaction
from .service import create_transaction_id, get_wallet_from_user
from wallet_application.mixins import AuthRequiredMixin
from .serializers import PaymentViewSerializer
logger = logging.getLogger(__name__)


class PaymentView(AuthRequiredMixin, APIView):

    @transaction.atomic
    def post(self, request):
        serializer = PaymentViewSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        wallet = get_wallet_from_user(request.user)
        amount, action = serializer.data['amount'], serializer.data['action']
        if action == 'add' and amount:
            payment_attempt = Transaction.objects.create(wallet=wallet, amount=amount, payment_type='credit',
                                                         transaction_id=create_transaction_id(),
                                                         status='processing')
            wallet.wallet_amount = wallet.wallet_amount + amount
            wallet.save()
            payment_attempt.status = 'success'
            payment_attempt.save()
            return Response({'success': True, 'msg': 'Money added to wallet succesfully'})
        elif action == 'pay' and amount:
            contact_username = request.POST.get('contact_username', None)
            if wallet.wallet_amount < amount:
                return Response({'success': False, 'msg': 'Wallet does not have sufficient balance'})
            if not contact_username:
                return Response({'success': False, 'msg': 'Please provide contact_username field'})
            try:
                contact_user_obj = User.objects.get(username=contact_username)
            except User.DoesNotExist:
                return Response({'success': False, 'msg': 'User does not exist'})
            else:
                contact_wallet_obj = get_wallet_from_user(contact_user_obj)
                payment_attempt = Transaction.objects.create(wallet=wallet, amount=amount, payment_type='debit',
                                                             transaction_id=create_transaction_id(), status='processing'
                                                             , credit_or_payer_wallet=contact_wallet_obj)
                try:
                    contact_wallet_obj.wallet_amount = contact_wallet_obj.wallet_amount + amount
                    wallet.wallet_amount = wallet.wallet_amount - amount
                    contact_wallet_obj.save()
                    wallet.save()
                    payment_attempt.status = 'success'
                    payment_attempt.save()
                    success, msg = True, 'Payment made successfully'
                except Exception as e:
                    logger.error("Error while processing payment {}: {}".format(payment_attempt.transaction_id, e))
                    payment_attempt.status = 'failed'
                    payment_attempt.save()
                    success, msg = False, 'Payment failed. Please try again'
                return Response({'success': success, 'msg': msg})
        else:
            return Response({'sucess': False, 'msg': 'Invalid action'})


class BalanceView(AuthRequiredMixin, APIView):

    def get(self, request):
        wallet = get_wallet_from_user(request.user)
        context = {'wallet_amount': wallet.wallet_amount, 'username': request.user.username}
        return Response({'success': True, 'data': context})
