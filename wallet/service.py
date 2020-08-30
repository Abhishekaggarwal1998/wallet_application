import random
from datetime import datetime
from .models import Wallet


def create_transaction_id():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return '%s%s' % (timestamp, random.randint(1000, 9999))


def get_wallet_from_user(user_obj):
    try:
        wallet = Wallet.objects.get(user=user_obj)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=user_obj)
    return wallet
