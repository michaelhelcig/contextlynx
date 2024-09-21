# Generated by Django 5.1.1 on 2024-09-21 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodenote',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='edge',
            name='similarity',
            field=models.FloatField(null=True),
        ),
    ]
