from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from transacoes.views import (
    ReceitasViewSet,
    ReceitasAnoMes,
    ReceitasId,
    DespesasViewSet,
    DespesasId,
    DespesasAnoMes,
    SummaryView)

urlpatterns = [
    path('receitas/', ReceitasViewSet.as_view()),
    path('receitas/<str:id>/', ReceitasId.as_view()),
    path('receitas/<int:ano>/<int:mes>/', ReceitasAnoMes.as_view()),
    path('despesas/', DespesasViewSet.as_view()),
    path('despesas/<int:id>/', DespesasId.as_view()),
    path('despesas/<int:ano>/<int:mes>/', DespesasAnoMes.as_view()),
    path('resumo/<int:ano>/<int:mes>/', SummaryView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
