# Generated by Django 3.0.7 on 2020-07-10 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sup_med', '0010_auto_20200710_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sup_info',
            name='logo',
            field=models.CharField(default='static/sup_med/空.jpg', max_length=50),
        ),
    ]
