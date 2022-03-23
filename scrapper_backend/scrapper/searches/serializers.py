from rest_framework import serializers
from searches.models import Search


class SearchesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Search
        fields = '__all__'
