from rest_framework import serializers
from .models import RealEstateAd

class RealEstateAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstateAd
        fields = '__all__'
