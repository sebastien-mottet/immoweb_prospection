import datetime

from rest_framework import serializers
from prospection.models import ProspectionRule, ProspectionLog
from properties.models import Property


class ProspectionRulesSerializer(serializers.ModelSerializer):

    properties = serializers.SerializerMethodField()

    def get_properties(self, obj):
        limit_date = datetime.date.today() - datetime.timedelta(obj.delay)
        logs = ProspectionLog.objects.filter(rule=obj.id)
        excluded_codes = [log.property.immoweb_code for log in logs]
        properties = Property.objects.exclude(immoweb_code__in=excluded_codes).filter(
            has_agency=obj.has_agency).filter(create_date__lte=limit_date)
        return [property.immoweb_code for property in properties]

    class Meta:
        model = ProspectionRule
        fields = '__all__'


class ProspectionLogsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProspectionLog
        fields = '__all__'
