from transacoes.models import Receitas, Despesas
from rest_framework.views import APIView
from transacoes.serializers import ReceitasSerializer, DespesasSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


class ReceitasList(APIView):
    """
    Lista todas as receitas cadastradas
    """

    def get(self, request, format=None):
        receitas = Receitas.objects.all()
        serializer = ReceitasSerializer(receitas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReceitasSerializer(data=request.data)

        # Validando serializer e conferindo se já existe uma receita com a mesma descrição no mesmo mês/ano

        if serializer.is_valid():
            descricao_request = request.data['descricao']
            data_request = request.data['data']
            data_request_mes = data_request.split('-')[1]
            data_request_ano = data_request.split('-')[0]

            if Receitas.objects.filter(data__year=data_request_ano, data__month=data_request_mes).exists() and Receitas.objects.filter(descricao=descricao_request).exists():
                return Response({'error': 'Receita já registrada no mesmo mês/ano'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReceitaDetail(APIView):
    """
    Apresenta, atualiza ou deleta a instância Receita.
    """

    def get_object(self, pk):
        try:
            return Receitas.objects.get(pk=pk)
        except Receitas.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        receitas = self.get_object(pk)
        serializer = ReceitasSerializer(receitas)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        receitas = self.get_object(pk)
        serializer = ReceitasSerializer(receitas, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        receitas = self.get_object(pk)
        receitas.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DespesasList(APIView):
    """
    Lista todas as despesas cadastradas
    """

    def get(self, request, format=None):
        despesas = Despesas.objects.all()
        serializer = DespesasSerializer(despesas, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DespesasSerializer(data=request.data)

        # Validando serializer e conferindo se já existe uma despesa com a mesma descrição no mesmo mês/ano

        if serializer.is_valid():
            descricao_request = request.data['descricao']
            data_request = request.data['data']
            data_request_mes = data_request.split('-')[1]
            data_request_ano = data_request.split('-')[0]

            if Despesas.objects.filter(data__year=data_request_ano, data__month=data_request_mes).exists() and Despesas.objects.filter(descricao=descricao_request).exists():
                return Response({'error': 'Despesa já registrada no mesmo mês/ano'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DespesaDetail(APIView):
    """
    Apresenta, atualiza ou deleta a instância Despesa.
    """

    def get_object(self, pk):
        try:
            return Despesas.objects.get(pk=pk)
        except Despesas.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        despesas = self.get_object(pk)
        serializer = DespesasSerializer(despesas)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        despesas = self.get_object(pk)
        serializer = DespesasSerializer(despesas, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        despesas = self.get_object(pk)
        despesas.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
