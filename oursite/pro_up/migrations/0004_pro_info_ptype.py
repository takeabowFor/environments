# Generated by Django 3.0.7 on 2020-06-27 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_up', '0003_pro_info_sid'),
    ]

    operations = [
        migrations.AddField(
            model_name='pro_info',
            name='ptype',
            field=models.CharField(default='', max_length=50),
        ),
    ]
