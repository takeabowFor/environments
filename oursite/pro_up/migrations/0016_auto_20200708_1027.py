# Generated by Django 3.0.7 on 2020-07-08 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_up', '0015_auto_20200708_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pro_info',
            name='p_picture',
            field=models.ImageField(upload_to='static/pro_md/%Y%m%d'),
        ),
    ]
