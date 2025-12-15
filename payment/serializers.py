from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields =[
            "phoneNumber",
            "amount",
            "status",
            "transactionId",
            "paymentMethod"
        ]

class StudentPaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id',
            'amount',
            'phoneNumber',
            'transactionId',
            'paymentMethod',
            'status',
            'createdAt',
        ]