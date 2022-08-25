from django.db import models


class Receitas(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.FloatField()
    data = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.descricao


class CategoriasDespesasEnum(models.TextChoices):
    ALIMENTACAO = "Alimentação"
    SAUDE = "Saúde"
    MORADIA = "Moradia"
    TRANSPORTE = "Transporte"
    EDUCACAO = "Educação"
    LAZER = "Lazer"
    IMPREVISTOS = "Imprevistos"
    OUTRAS = "Outras"


class Despesas(models.Model):

    descricao = models.CharField(max_length=200)
    valor = models.FloatField()
    categoria = models.CharField(
        max_length=11,
        null=False,
        blank=False,
        choices=CategoriasDespesasEnum.choices,
        default=CategoriasDespesasEnum.OUTRAS)
    data = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.descricao
