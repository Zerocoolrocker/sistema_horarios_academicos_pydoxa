# Generated by Django 2.2.6 on 2019-10-02 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dia',
            name='nombre',
            field=models.IntegerField(),
        ),
    ]
