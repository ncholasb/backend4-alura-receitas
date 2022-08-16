from transacoes.models import Receitas, Despesas
from transacoes.serializers import ReceitasSerializer, DespesasSerializer, ReceitaListSerializer, DespesaListSerializer  # noqa
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics
from django.db.models import Sum

# Create your views here.


class ReceitaViewSet(viewsets.ModelViewSet):
    '''
    Lista todas as receitas registradas
    '''
    queryset = Receitas.objects.all()
    serializer_class = ReceitasSerializer

    def get_queryset(self):
        queryset = Receitas.objects.all()
        descricao = self.request.query_params.get('descricao')

        if descricao:
            queryset = queryset.filter(descricao__icontains=descricao)
        return queryset


class DespesaViewSet(viewsets.ModelViewSet):
    '''
    Lista todas as despesas registradas
    '''
    queryset = Despesas.objects.all()
    serializer_class = DespesasSerializer

    def get_queryset(self):
        queryset = Receitas.objects.all()
        descricao = self.request.query_params.get('descricao')

        if descricao:
            queryset = queryset.filter(descricao__icontains=descricao)
        return queryset


class ReceitaList(generics.ListAPIView):
    '''
    Exibe a receita registrada que cumpre o critério de busca,
    passado por parâmetro
    '''

    serializer_class = ReceitaListSerializer

    def get_queryset(self):
        queryset = Receitas.objects.filter(data__year=self.kwargs['year'],
                                           data__month=self.kwargs['month'])
        return queryset


class DespesaList(generics.ListAPIView):
    '''
    Exibe a despesa registrada que cumpre o critério de busca,
    passado por parâmetro
    '''
    serializer_class = DespesaListSerializer

    def get_queryset(self):
        queryset = Despesas.objects.filter(data__year=self.kwargs['year'],
                                           data__month=self.kwargs['month'])
        return queryset


class SummaryView(APIView):
    '''
    Exibe o resumo de receitas e despesas registradas
    '''
    queryset = Receitas.objects.none()

    def get(self, request, month, year, format=None):
        receita_month = Receitas.objects.filter(data__month=month, data__year=year).aggregate(Sum('valor'))['valor__sum'] or 0  # noqa
        despesa_month = Despesas.objects.filter(data__month=month, data__year=year).aggregate(Sum('valor'))['valor__sum'] or 0  # noqa
        total = receita_month - despesa_month
        category_despesa = Despesas.objects.filter(data__month=month, data__year=year).values('categoria').annotate(total_valor=Sum('valor'))  # noqa

        return Response({
            'Receita no mês': f'R$ {receita_month}',
            'Despesa no mês': f'R$ {despesa_month}',
            'Saldo final': f'R$ {total}',
            'Categorias de despesa': category_despesa

        })
