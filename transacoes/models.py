from django.db import models


class Receitas(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(
        decimal_places=2, max_digits=8, null=False, blank=False)
    data = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.descricao


class Despesas(models.Model):
    CATEGORIA_CHOICES = (
        ('1', 'Alimentação'),
        ('2', 'Saúde'),
        ('3', "Moradia"),
        ("4", "Transporte"),
        ("5", "Educação"),
        ("6", "Lazer"),
        ("7", "Imprevistos"),
        ("8", "Outras"),
    )

    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(decimal_places=2, max_digits=15, null=False, blank=False)  # noqa
    categoria = models.CharField(max_length=15, null=False, blank=False, choices=CATEGORIA_CHOICES, default='Outras')  # noqa
    data = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.descricao
