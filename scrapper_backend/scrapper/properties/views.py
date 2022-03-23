from rest_framework import viewsets

from properties.models import Property
from properties.serializers import PropertiesSerializer


class PropertiesViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertiesSerializer
