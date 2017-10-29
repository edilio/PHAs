from rest_framework import serializers
from .models import Pha


class PhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pha
        fields = '__all__'
