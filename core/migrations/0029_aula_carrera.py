# Generated by Django 2.2.4 on 2020-01-17 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_proyecto_pensum'),
    ]

    operations = [
        migrations.AddField(
            model_name='aula',
            name='carrera',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Carrera'),
        ),
    ]
