from rest_framework import viewsets

from prospection.models import ProspectionRule, ProspectionLog
from prospection.serializers import ProspectionRulesSerializer, ProspectionLogsSerializer

class ProspectionRulesViewSet(viewsets.ModelViewSet):
    queryset = ProspectionRule.objects.all()
    serializer_class = ProspectionRulesSerializer


class ProspectionLogsViewSet(viewsets.ModelViewSet):
    queryset = ProspectionLog.objects.all()
    serializer_class = ProspectionLogsSerializer
