from transacoes.views import ReceitasViewSet, ReceitasAnoMes, ReceitasId, DespesasViewSet, DespesasId, DespesasAnoMes, SummaryView  # noqa
from django.urls import path


urlpatterns = [
    path('receitas/', ReceitasViewSet.as_view()),
    path('receitas/<str:id>/', ReceitasId.as_view()),
    path('receitas/<int:ano>/<int:mes>/', ReceitasAnoMes.as_view()),
    path('despesas/', DespesasViewSet.as_view()),
    path('despesas/<int:id>/', DespesasId.as_view()),
    path('despesas/<int:ano>/<int:mes>/', DespesasAnoMes.as_view()),
    path('resumo/<int:ano>/<int:mes>/', SummaryView.as_view()),
]
