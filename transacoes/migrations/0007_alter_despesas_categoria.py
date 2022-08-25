# Generated by Django 4.0.6 on 2022-08-25 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transacoes', '0006_alter_receitas_valor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despesas',
            name='categoria',
            field=models.CharField(choices=[('Alimentação', 'Alimentacao'), ('Saúde', 'Saude'), ('Moradia', 'Moradia'), ('Transporte', 'Transporte'), ('Educação', 'Educacao'), ('Lazer', 'Lazer'), ('Imprevistos', 'Imprevistos'), ('Outras', 'Outras')], default='Outras', max_length=11),
        ),
    ]
