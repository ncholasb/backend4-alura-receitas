from transacoes import views
from django.urls import path, include


urlpatterns = [
    path('receitas/', views.ReceitasList.as_view()),
    path('receitas/<int:pk>/', views.ReceitaDetail.as_view()),
    path('despesas/', views.DespesasList.as_view()),
    path('despesas/<int:pk>/', views.DespesaDetail.as_view()),
]
