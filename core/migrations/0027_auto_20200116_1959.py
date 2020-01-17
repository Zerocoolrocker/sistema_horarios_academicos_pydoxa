# Generated by Django 2.2.4 on 2020-01-16 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20200106_2058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrera',
            name='area',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='area',
        ),
        migrations.RemoveField(
            model_name='esquemabloque',
            name='area',
        ),
        migrations.RemoveField(
            model_name='esquemadia',
            name='area',
        ),
        migrations.RemoveField(
            model_name='restriccionesbloques',
            name='area',
        ),
        migrations.AddField(
            model_name='docente',
            name='carrera',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Carrera'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='esquemabloque',
            name='carrera',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Carrera'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='esquemadia',
            name='carrera',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Carrera'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restriccionesbloques',
            name='carrera',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.Carrera'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ubicacionaula',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Aula'),
        ),
    ]