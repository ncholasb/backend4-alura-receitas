from rest_framework import serializers
from transacoes.models import Receitas, Despesas


class ReceitasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receitas
        fields = ('id', 'descricao', 'valor', 'data')
        ordering = ['-id']


class DespesasSerializer(serializers.ModelSerializer):
    # categoria = CategoriaField(source="*")

    class Meta:
        model = Despesas
        fields = ('id', 'descricao', 'valor', 'categoria', 'data')
        ordering = ['-id']

    # Se categoria não vier especificada, então assume-se que é Outras

    def to_representation(self, instance):
        dado = super().to_representation(instance)
        if not dado.get('categoria'):
            dado['categoria'] = 'Outras'
        return dado
