from rest_framework import serializers
from properties.models import Property


class PropertiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = '__all__'
