from rest_framework import serializers
from .models import reviewForm


class reviewFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = reviewForm
        fields = '__all__'
