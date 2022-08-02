from rest_framework.viewsets import ModelViewSet

from transacoes.models import Receitas
from transacoes.serializers import ReceitasSerializer


class ReceitasViewSet(ModelViewSet):
    serializer_class = ReceitasSerializer

    def get_queryset(self):
        return Receitas.objects.all().order_by('id')
