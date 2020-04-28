from rest_framework import serializers
from backend.models import Lawyer, Inquiry, Answer
from django.contrib.auth import get_user_model

class userProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = get_user_model()
        fields = '__all__'