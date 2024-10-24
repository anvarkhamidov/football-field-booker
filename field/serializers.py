from rest_framework import serializers

from field.models import Field


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['id', 'name', 'address', 'contact_info', 'coordinates', 'hourly_rate', 'images']
