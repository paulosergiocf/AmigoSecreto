# Generated by Django 4.2.7 on 2023-12-04 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amigoSecreto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salasorteio',
            name='codigoSala',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amigoSecreto.sala', unique=True),
        ),
    ]