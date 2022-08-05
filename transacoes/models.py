from django.db import models


class Receitas(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(
        decimal_places=2, max_digits=8, null=False, blank=False)
    data = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.descricao


class Despesas(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(
        decimal_places=2, max_digits=15, null=False, blank=False)
    data = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.descricao
