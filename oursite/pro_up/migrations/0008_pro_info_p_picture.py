# Generated by Django 3.0.7 on 2020-06-27 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_up', '0007_auto_20200627_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='pro_info',
            name='p_picture',
            field=models.ImageField(default='', upload_to='pro_up/'),
        ),
    ]
