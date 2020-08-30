from django.db import models
from decimal import Decimal


class Wallet(models.Model):
    user = models.OneToOneField('auth.User', related_name='wallet', on_delete=models.CASCADE)
    wallet_amount = models.DecimalField(max_digits=22, decimal_places=2, default=Decimal(0))


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, related_name='user_wallet', null=True, blank=True, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    amount = models.DecimalField(max_digits=22, decimal_places=2, default=Decimal(0))
    payment_type = models.CharField(max_length=50, choices=(
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ))
    status = models.CharField(max_length=50, default='pending', choices=(
        ('failed', 'Failed'),
        ('success', 'Success'),
        ('processing', 'Processing'),
        ('pending', 'Pending')
    ))
    # field to check whom user has paid or from whom money has been credited
    credit_or_payer_wallet = models.ForeignKey(Wallet, related_name='credit_or_payer_wallet', null=True, blank=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

