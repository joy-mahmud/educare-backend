from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields =[
            "phoneNumber",
            "amount",
            "payment_breakdown",
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
class AdminPaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "phoneNumber",
            "amount",
            "status",
            "transactionId",
            "paymentMethod",
            "createdAt",
        ]
class PaymentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['status']
class SinglePaymentGetSerializer(serializers.ModelSerializer):
    class Meta:
        model= Payment
        fields = "__all__"