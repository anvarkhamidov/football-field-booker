from rest_framework import serializers

from field.models import Field


class FieldSerializer(serializers.HyperlinkedModelSerializer):
    distance = serializers.SerializerMethodField()
    price_per_hour = serializers.FloatField()

    class Meta:
        model = Field
        fields = [
            "id",
            "name",
            "address",
            "contact_info",
            "longitude",
            "latitude",
            "price_per_hour",
            "images",
            "description",
            "available_from",
            "available_to",
            "distance",
        ]

    def get_distance(self, obj):
        return getattr(obj, "distance", None)

    def to_representation(self, instance):
        # Remove 'distance' field for actions other than 'list'
        representation = super().to_representation(instance)
        action = self.context.get("action")
        if action != "list":
            representation.pop(
                "distance", None
            )  # Remove distance for non-list actions
        return representation
