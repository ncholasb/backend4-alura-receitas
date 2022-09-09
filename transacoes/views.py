from django.middleware import csrf
from rest_framework_simplejwt.tokens import RefreshToken
from transacoes.models import Receitas, Despesas
from transacoes.serializers import (
    ReceitasSerializer,
    DespesasSerializer,
    UserRegistrySerializer,
    UserLoginSerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, AllowAny
import uuid


class ReceitasViewSet(APIView):
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

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
                data={
                    "error": f"Não foi encontrada nenhuma despesa com id: {id}"
                }
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
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    def get(self, request, ano, mes):
        receitas_total = self.get_receitas_total(ano, mes)
        despesas_total = self.get_despesas_total(ano, mes)
        saldo_final = receitas_total - despesas_total
        total_gasto_por_categoria = self.get_total_gasto_categoria(ano, mes)
        return Response(data={
            "Receitas total": receitas_total,
            "Despesas total": despesas_total,
            "Saldo final": saldo_final,
            "Gasto total por categoria": total_gasto_por_categoria
        }, status=status.HTTP_200_OK)

    def get_despesas_total(self, ano, mes):
        despesas = Despesas.objects.filter(data__year=ano, data__month=mes)
        value: float = 0
        for row in despesas:
            value += row.valor
        return value

    def get_receitas_total(self, ano, mes):
        receitas = Receitas.objects.filter(data__year=ano, data__month=mes)
        value: float = 0
        for row in receitas:
            value += row.valor
        return value

    def get_total_gasto_categoria(self, ano, mes):
        despesas = Despesas.objects.filter(data__year=ano, data__month=mes)
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


class UserRegistryViewSet(generics.GenericAPIView):
    '''Cria usuários'''
    serializer_class = UserRegistrySerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response({
                "RequestID": str(uuid.uuid4()),
                "Message": "User created successfully",
                "User": serializer.data}, status=status.HTTP_201_CREATED
            )

        return Response(
            {"Errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        data = request.data
        response = Response()
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(
            username=username, password=password
        )

        if user is not None:
            data = get_tokens_for_user(user)
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=data["access"],
                expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
            csrf.get_token(request)
            response.data = {"Success": "Login successfully", "data": data}

            return response
        else:
            return Response({"Invalid": "Invalid username or password!!"},
                            status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):

    def get(self, request):
        response = Response()

        response.delete_cookie('access_token')
        response.data = {
            'message': 'success, cookies of auth deleted'
        }

        return response
