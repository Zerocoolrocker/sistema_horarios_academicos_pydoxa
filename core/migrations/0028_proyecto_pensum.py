# Generated by Django 2.2.4 on 2020-01-16 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20200116_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='pensum',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Pensum'),
            preserve_default=False,
        ),
    ]
