from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from core.permissions import IsFieldOwner
from field.filters import FieldFilter
from field.geo_utils import calculate_distance
from field.models import Field
from field.serializers import FieldSerializer


class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = FieldSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = FieldFilter

    def get_permissions(self):
        # Allow all users to list and retrieve fields
        if self.action in ["list", "retrieve"]:
            return [permissions.IsAuthenticated()]
        # Allow only field owners to update, delete and create fields
        return [
            permissions.IsAuthenticated(),
            permissions.IsAdminUser(),
            IsFieldOwner(),
        ]

    def list(self, request, *args, **kwargs):
        user_lat = request.query_params.get("latitude")
        user_lon = request.query_params.get("longitude")

        # Filter by query params
        fields = self.filter_queryset(self.get_queryset())

        if user_lat is not None and user_lon is not None:
            try:
                user_lat = float(user_lat)
                user_lon = float(user_lon)
            except ValueError:
                return Response({"error": "Invalid coordinates"}, status=400)

            for field in fields:
                distance_km = round(
                    calculate_distance(
                        user_lat, user_lon, field.latitude, field.longitude
                    ),
                    2,
                )
                field.distance = f"{distance_km} km"

            # Sort by distance in KM
            fields = sorted(fields, key=lambda x: x.distance)
        else:
            # Sort by id after other filters if no location given
            fields = sorted(fields, key=lambda x: x.id)

        # Serialize
        serializer = self.get_serializer(fields, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Automatically assign the owner of the field to the current user
        serializer.save(owner=self.request.user)

    def get_serializer_context(self):
        # Pass the action type to the serializer context
        context = super().get_serializer_context()
        context["action"] = self.action
        return context
