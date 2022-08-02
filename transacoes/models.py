from django.db import models

# Create your models here.


class Receitas(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.FloatField(null=False, blank=False)
    data = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.descricao


class Despesas(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.FloatField(null=False, blank=False)
    data = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.descricao
