# Generated by Django 2.2.4 on 2020-02-04 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200204_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='materia',
            name='semestre',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]