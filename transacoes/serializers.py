from dataclasses import fields
from rest_framework import serializers
from transacoes.models import Receitas, Despesas
from django.contrib.auth.models import User


class ReceitasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receitas
        fields = ('id', 'descricao', 'valor', 'data')
        ordering = ['-id']


class DespesasSerializer(serializers.ModelSerializer):
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


class UserRegistrySerializer(serializers.ModelSerializer):
    '''Serializer para Usuário'''
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True},
        }

    def create(self, validated_data):
        '''Cria e retorna um usuário'''
        usuario = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'username': {'required': True},
        }
