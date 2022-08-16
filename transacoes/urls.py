from transacoes.views import ReceitaViewSet, DespesaViewSet, ReceitaList, DespesaList, SummaryView  # noqa
from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()

router.register('receitas', ReceitaViewSet, basename='receitas')
router.register('despesas', DespesaViewSet, basename='despesas')

urlpatterns = [
    path('', include(router.urls)),
    path('receitas/<int:year>/<int:month>/', ReceitaList.as_view()),
    path('despesas/<int:year>/<int:month>/', DespesaList.as_view()),
    path('resumo/<int:year>/<int:month>/', SummaryView.as_view()),
]
