# Generated by Django 5.1.1 on 2024-09-19 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodenote',
            name='icon',
            field=models.CharField(default='🗒', max_length=16),
        ),
    ]