from rest_framework import serializers
from transacoes.models import Receitas, Despesas


class ReceitasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receitas
        fields = ('id', 'descricao', 'valor', 'data')


class DespesasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesas
        fields = ('id', 'descricao', 'valor', 'data')
