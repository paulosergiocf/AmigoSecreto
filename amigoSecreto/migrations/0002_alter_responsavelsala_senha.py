# Generated by Django 4.2.7 on 2023-12-03 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amigoSecreto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsavelsala',
            name='senha',
            field=models.CharField(max_length=128),
        ),
    ]
