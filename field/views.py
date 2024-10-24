from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from field.models import Field
from field.serializers import FieldSerializer


class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsAuthenticated()]
        return []
