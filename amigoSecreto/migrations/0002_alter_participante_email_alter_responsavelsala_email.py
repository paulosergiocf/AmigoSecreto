# Generated by Django 4.2.7 on 2023-12-08 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amigoSecreto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participante',
            name='email',
            field=models.EmailField(max_length=320, unique=True),
        ),
        migrations.AlterField(
            model_name='responsavelsala',
            name='email',
            field=models.EmailField(max_length=320, unique=True),
        ),
    ]