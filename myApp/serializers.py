from rest_framework import serializers
from .models import NganhTuyenSinh

class NganhTuyenSinhSerializer(serializers.ModelSerializer):
    class Meta:
        model = NganhTuyenSinh
        fields = '__all__' 