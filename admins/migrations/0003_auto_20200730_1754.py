# Generated by Django 3.0.8 on 2020-07-30 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0002_auto_20200730_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anuncios',
            name='reservado',
            field=models.BooleanField(null=True),
        ),
    ]
