import datetime
from rest_framework import serializers
from django.core.validators import RegexValidator
from django.db.models import Q
from wallet.models import Transaction, Wallet


def mobile_number_restrictions(mobile_no):
    return RegexValidator(
        regex='^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[6789]\d{9}|(\d[ -]?){10}\d$',
        message='Phone number can only contain numbers and should be 10 digits or enter valid mobile number',
        code='invalid_phone_no'
    )(mobile_no)


class BaseLoginRegisterRequestSerializer(serializers.Serializer):
    phone_no = serializers.CharField(max_length=50, validators=[mobile_number_restrictions])
    password = serializers.CharField(min_length=8)


class RegisterFormSerializer(BaseLoginRegisterRequestSerializer):
    first_name = serializers.CharField(min_length=5, max_length=50)
    last_name = serializers.CharField(required=False,min_length=5, max_length=50, allow_blank=True)


class TransactionListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        data = super(TransactionListSerializer, self).to_representation(instance)
        data['my_username'] = self.context.get('user').username
        data['credit_or_payer_username'] = None if not instance.credit_or_payer_wallet else instance.wallet.user.username if \
            instance.credit_or_payer_wallet == self.context.get('user').wallet else instance.credit_or_payer_wallet.user.username
        data['state'] = 'added money to wallet' if not instance.credit_or_payer_wallet else 'credited' if \
            instance.credit_or_payer_wallet == self.context.get('user').wallet else "debited"
        data.pop('payment_type')
        return data

    class Meta:
        model = Transaction
        fields = '__all__'


class UserCurrentMonthDetailsSerializer(serializers.Serializer):

    def to_representation(self, instance):
        data = super(UserCurrentMonthDetailsSerializer, self).to_representation(instance)
        data['username'] = instance.username
        data['wallet_id'] = instance.wallet.id
        data['current_balance'] = instance.wallet.wallet_amount
        start_of_month = datetime.date.today().replace(day=1)
        credit_transaction_list = Transaction.objects.filter(Q(payment_type='credit', wallet=instance.wallet) | Q(credit_or_payer_wallet=
                                                             instance.wallet), created_on__gte=start_of_month, status='success')
        data['credit_amount'] = sum(transaction.amount for transaction in credit_transaction_list)
        debit_transaction_list = Transaction.objects.filter(
            payment_type='debit', wallet=instance.wallet, created_on__gte=start_of_month, status='success')
        data['debit_amount'] = sum(transaction.amount for transaction in debit_transaction_list)
        return data
