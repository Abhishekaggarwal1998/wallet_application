# Generated by Django 3.1 on 2020-08-30 02:44

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet_amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=22)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=22)),
                ('payment_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=50)),
                ('status', models.CharField(choices=[('failed', 'Failed'), ('success', 'Success'), ('processing', 'Processing'), ('pending', 'Pending')], default='pending', max_length=50)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('credit_or_payer_wallet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credit_or_payer_wallet', to='wallet.wallet')),
                ('wallet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_wallet', to='wallet.wallet')),
            ],
        ),
    ]