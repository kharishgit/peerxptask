# Generated by Django 4.1.5 on 2023-01-14 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='support.department'),
        ),
    ]
