from rest_framework import viewsets

from searches.models import Search
from searches.serializers import SearchesSerializer


class SearchesViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchesSerializer
