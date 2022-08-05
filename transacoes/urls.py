from transacoes import views
from django.urls import path, include


urlpatterns = [
    path('receitas/', views.ReceitasList.as_view()),
    path('receitas/<int:pk>/', views.ReceitaDetail.as_view()),
    path('despesas/', views.DespesasList.as_view()),
    path('despesas/<int:pk>/', views.DespesaDetail.as_view()),
]

'''
router = routers.SimpleRouter()

router.register(r'receitas', views.Receitas.as_view())
router.register(r'despesas', views.Despesas.as_view())

urlpatterns = [
    path("", include(router.urls)),
]
'''

'''
urlpatterns = [
    path('receitas/', views.receita, name='receita'),
    path('receitas/<str:id>/', views.detalha_receita, name='detalha_receita'),
    path('despesas/', views.despesa, name='despesa'),
    path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
'''
