# Generated by Django 3.0.7 on 2020-07-10 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_md', '0004_auto_20200701_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='uimage',
            field=models.CharField(default='static/user_md/空.jpg', max_length=256),
        ),
    ]
