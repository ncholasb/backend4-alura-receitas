# Generated by Django 4.0.6 on 2022-08-24 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transacoes', '0004_despesas_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despesas',
            name='valor',
            field=models.FloatField(),
        ),
    ]
