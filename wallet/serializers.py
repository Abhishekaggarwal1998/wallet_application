from rest_framework import serializers


def amount_validate(amount):
    if amount < 1:
        raise serializers.ValidationError("Please enter a valid amount")
    return amount


class PaymentViewSerializer(serializers.Serializer):
    amount = serializers.IntegerField(validators=[amount_validate])
    action = serializers.CharField()