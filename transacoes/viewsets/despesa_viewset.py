from rest_framework.viewsets import ModelViewSet

from transacoes.models import Despesas
from transacoes.serializers import DespesasSerializer


class DespesasViewSet(ModelViewSet):
    serializer_class = DespesasSerializer

    def get_queryset(self):
        return Despesas.objects.all().order_by('id')
