# Generated by Django 2.2.6 on 2019-10-05 22:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20191005_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='seccion',
            name='bloque',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Bloque'),
            preserve_default=False,
        ),
    ]
