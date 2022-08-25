from transacoes.models import Receitas, Despesas
from transacoes.serializers import ReceitasSerializer, DespesasSerializer, ReceitaListSerializer, DespesaListSerializer  # noqa
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ReceitasViewSet(APIView):
    def get(self, request):
        if request.GET.get("descricao"):
            receitas = Receitas.objects.filter(
                descricao__contains=request.GET.get("descricao")
            )
            return Response(data=ReceitasSerializer(receitas, many=True).data)
        else:
            receitas = Receitas.objects.all()
            if len(receitas) >= 1:
                serializer = ReceitasSerializer(receitas, many=True)
                return Response(
                    status=status.HTTP_200_OK,
                    data=serializer.data
                )
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"error": "Não há dados cadastrados"}
                )

    def post(self, request):
        serializer = ReceitasSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                status=status.HTTP_200_OK,
                data={"message": "Dados registrados!"}
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"error": "Os dados não foram registrados..."}
        )


class ReceitasId(APIView):
    def get(self, request, id):
        try:
            receitas = Receitas.objects.get(id=id)
            serializer = ReceitasSerializer(receitas)
            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        except Receitas.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": f"Não foi encontrada nenhuma receita com id: {id}"}  # noqa
            )

    def delete(self, request, id):
        if Receitas.objects.filter(id=id):
            Receitas.objects.filter(id=id).delete()
            return Response(
                {"message": f"Receita {id} removida com sucesso!"}
            )
        else:
            return Response(
                {"error": f"Não foi encontrada nenhuma receita com id: {id}"}
            )

    def put(self, request, id):
        try:
            receita = Receitas.objects.get(id=id)
            receita.id = request.data.get("id")
            receita.descricao = request.data.get("descricao")
            receita.valor = request.data.get("valor")
            receita.data = request.data.get("data")
            receita.save()
            return Response({"message": "Receita atualizada com sucesso!"})
        except Receitas.DoesNotExist:
            return Response(
                {"error": f"Não foi encontrada nenhuma receita com id: {id}"}
            )


class ReceitasAnoMes(APIView):
    def get(self, request, ano, mes):
        receitas = Receitas.objects.filter(data__year=ano) & Receitas.objects.filter(data__month=mes)  # noqa
        if receitas.count() != 0:
            return Response(
                data=ReceitasSerializer(receitas, many=True).data
            )
        else:
            return Response(
                {"error": f"Não foram encontradas receitas no mês: {mes} e ano: {ano}"}  # noqa
            )


class DespesasViewSet(APIView):
    def get(self, request):
        if request.GET.get("descricao"):
            despesas = Despesas.objects.filter(
                descricao__contains=request.GET.get("descricao")
            )
            return Response(data=DespesasSerializer(despesas, many=True).data)
        else:
            despesas = Despesas.objects.all()
            if len(despesas) >= 1:
                serializer = DespesasSerializer(despesas, many=True)
                return Response(
                    status=status.HTTP_200_OK,
                    data=serializer.data
                )
            else:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"error": "Não há dados cadastrados"}
                )

    def post(self, request):
        serializer = DespesasSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                status=status.HTTP_200_OK,
                data={"message": "Dados registrados!"}
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"error": "Os dados não foram registrados..."}
        )


class DespesasId(APIView):
    def get(self, request, id):
        try:
            despesas = Despesas.objects.get(id=id)
            serializer = DespesasSerializer(despesas)
            return Response(
                status=status.HTTP_200_OK,
                data=serializer.data
            )
        except Despesas.DoesNotExist:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": f"Não foi encontrada nenhuma despesa com id: {id}"}  # noqa
            )

    def delete(self, request, id):
        if Despesas.objects.filter(id=id):
            Despesas.objects.filter(id=id).delete()
            return Response(
                {"message": f"Despesa {id} removida com sucesso!"}
            )
        else:
            return Response(
                {"error": f"Não foi encontrada nenhuma despesa com id: {id}"}
            )

    def put(self, request, id):
        try:
            despesas = Despesas.objects.get(id=id)
            despesas.id = request.data.get("id")
            despesas.descricao = request.data.get("descricao")
            despesas.valor = request.data.get("valor")
            despesas.data = request.data.get("data")
            despesas.save()
            return Response({"message": "Despesa atualizada com sucesso!"})
        except Despesas.DoesNotExist:
            return Response(
                {"error": f"Não foi encontrada nenhuma Despesa com id: {id}"}
            )


class DespesasAnoMes(APIView):
    def get(self, request, ano, mes):
        despesas = Despesas.objects.filter(data__year=ano) & Despesas.objects.filter(data__month=mes)  # noqa
        if despesas.count() != 0:
            return Response(
                data=DespesasSerializer(despesas, many=True).data
            )
        else:
            return Response(
                {"error": f"Não foram encontradas despesas no mês: {mes} e ano: {ano}"}  # noqa
            )


class SummaryView(APIView):
    def get(self, request, ano, mes):
        receitas_total = self.get_receitas_total(ano, mes)
        despesas_total = self.get_despesas_total(ano, mes)
        saldo_final = receitas_total - despesas_total
        total_gasto_por_categoria = self.get_total_gasto_categoria(ano, mes)  # noqa
        return Response(data={
            "Receitas total": receitas_total,
            "Despesas total": despesas_total,
            "Saldo final": saldo_final,
            "Gasto total por categoria": total_gasto_por_categoria
        }, status=status.HTTP_200_OK)

    def get_despesas_total(self, ano, mes):
        despesas = Despesas.objects.filter(data__year=ano, data__month=mes)
        # despesas = Despesas.objects.filter(data__contains="{}-{}".format(ano, mes))  # noqa
        value: float = 0
        for row in despesas:
            value += row.valor
        return value

    def get_receitas_total(self, ano, mes):
        receitas = Receitas.objects.filter(data__year=ano, data__month=mes)
        #receitas = Receitas.objects.filter(data__contains="{}-{}".format(ano, mes))  # noqa
        value: float = 0
        for row in receitas:
            value += row.valor
        return value

    def get_total_gasto_categoria(self, ano, mes):
        despesas = Despesas.objects.filter(data__year=ano, data__month=mes)
       # despesas = Despesas.objects.filter(data__contains="{}-{}".format(ano, mes))  # noqa
        dict_categorias = self.get_dict_categorias()
        for row in despesas:
            dict_categorias[row.categoria] += row.valor
        return dict_categorias

    def get_dict_categorias(self) -> dict:
        return {
            "Alimentação": 0.0,
            "Saúde": 0.0,
            "Moradia": 0.0,
            "Transporte": 0.0,
            "Educação": 0.0,
            "Lazer": 0.0,
            "Imprevistos": 0.0,
            "Outras": 0.0
        }

# class ReceitaViewSet(viewsets.ModelViewSet):
#     '''
#     Lista todas as receitas registradas
#     '''
#     queryset = Receitas.objects.all()
#     serializer_class = ReceitasSerializer

#     def get_queryset(self):
#         queryset = Receitas.objects.all()
#         descricao = self.request.query_params.get('descricao')

#         if descricao:
#             queryset = queryset.filter(descricao__icontains=descricao)
#         return queryset

#     def create(self, request):
#         """
#         Regras para criação de uma nova receita.
#         Receitas com mesmo descricao em mesmo mês/ano não podem ser criadas.
#         """
#         descricao_request = request.data['descricao']
#         data_request = request.data['data']
#         data_request_mes = data_request.split('-')[1]
#         data_request_ano = data_request.split('-')[0]

#         if Receitas.objects.filter(data__year=data_request_ano, data__month=data_request_mes) & Receitas.objects.filter(descricao=descricao_request):  # noqa
#             return Response(
#                 {"error": "Receita já cadastrada no mesmo mês/ano"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         else:

#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             instance = self.perform_create(serializer)
#             serializer = self.get_serializer(instance=instance)

#             return Response(
#                 f"Receita '{descricao_request}' cadastrada com sucesso",
#                 status=status.HTTP_201_CREATED
#             )


# class ReceitaList(generics.ListAPIView):
#     '''
#     Exibe a receita registrada que cumpre o critério de busca,
#     passado por parâmetro
#     '''

#     serializer_class = ReceitaListSerializer

#     def get_queryset(self):
#         queryset = Receitas.objects.filter(data__year=self.kwargs['year'],
#                                            data__month=self.kwargs['month'])
#         return queryset


# class DespesaViewSet(viewsets.ModelViewSet):
#     '''
#     Lista todas as despesas registradas
#     '''
#     queryset = Despesas.objects.all()
#     serializer_class = DespesasSerializer

#     def get_queryset(self):
#         queryset = Receitas.objects.all()
#         descricao = self.request.query_params.get('descricao')

#         if descricao:
#             queryset = queryset.filter(descricao__icontains=descricao)
#         return queryset

#     def create(self, request):
#         """
#         Regras para criação de uma nova despesa.
#         Despesas com mesmo descricao em mesmo mês/ano não podem ser criadas.
#         """
#         descricao_request = request.data['descricao']
#         data_request = request.data['data']
#         data_request_mes = data_request.split('-')[1]
#         data_request_ano = data_request.split('-')[0]

#         if Despesas.objects.filter(data__year=data_request_ano, data__month=data_request_mes) & Despesas.objects.filter(descricao=descricao_request):  # noqa
#             return Response(
#                 {"error": "Despesa já cadastrada no mesmo mês/ano"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         else:

#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             instance = self.perform_create(serializer)
#             serializer = self.get_serializer(instance=instance)

#             return Response(
#                 f"Despesa '{descricao_request}' cadastrada com sucesso",
#                 status=status.HTTP_201_CREATED
#             )


# class DespesaList(generics.ListAPIView):
#     '''
#     Exibe a despesa registrada que cumpre o critério de busca,
#     passado por parâmetro
#     '''
#     serializer_class = DespesaListSerializer

#     def get_queryset(self):
#         queryset = Despesas.objects.filter(data__year=self.kwargs['year'],
#                                            data__month=self.kwargs['month'])
#         return queryset


# class SummaryView(APIView):
#     '''
#     Exibe o resumo de receitas e despesas registradas
#     '''
#     queryset = Receitas.objects.none()

#     def get(self, request, month, year, format=None):
#         receita_month = Receitas.objects.filter(data__month=month, data__year=year).aggregate(Sum('valor'))['valor__sum'] or 0  # noqa
#         despesa_month = Despesas.objects.filter(data__month=month, data__year=year).aggregate(Sum('valor'))['valor__sum'] or 0  # noqa
#         total = receita_month - despesa_month
#         category_despesa = Despesas.objects.filter(data__month=month, data__year=year).values('categoria').annotate(total_valor=Sum('valor'))  # noqa

#         return Response({
#             'Receita no mês': f'R$ {receita_month}',
#             'Despesa no mês': f'R$ {despesa_month}',
#             'Saldo final': f'R$ {total}',
#             'Categorias de despesa': category_despesa

#         })
