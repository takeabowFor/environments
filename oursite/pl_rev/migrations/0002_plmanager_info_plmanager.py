# Generated by Django 3.0.7 on 2020-07-08 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pl_rev', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plmanager_info',
            name='plmanager',
            field=models.CharField(default='', max_length=32),
        ),
    ]
