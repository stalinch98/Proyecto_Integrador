# Generated by Django 3.0.8 on 2020-07-29 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0002_contacto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='celular',
            field=models.CharField(max_length=10),
        ),
    ]