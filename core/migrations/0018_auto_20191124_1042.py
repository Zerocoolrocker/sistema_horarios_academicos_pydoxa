# Generated by Django 2.2.4 on 2019-11-24 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20191121_2033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bloque',
            name='esquema_dia',
        ),
        migrations.RemoveField(
            model_name='esquemabloque',
            name='dia',
        ),
        migrations.AddField(
            model_name='bloque',
            name='esquema_bloque',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.EsquemaBloque'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='esquemabloque',
            name='esquema_dia',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.EsquemaDia'),
            preserve_default=False,
        ),
    ]