from transacoes import viewsets
from django.urls import path, include
from rest_framework import routers
# from . import views

router = routers.SimpleRouter()

router.register(r'receitas', viewsets.ReceitasViewSet, basename='receitas')
router.register(r'despesas', viewsets.DespesasViewSet, basename='despesas')

urlpatterns = [
    path("", include(router.urls)),
]

'''
urlpatterns = [
    path('receitas/', views.receita, name='receita'),
    path('receitas/<str:id>/', views.detalha_receita, name='detalha_receita'),
    path('despesas/', views.despesa, name='despesa'),
    path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
'''
