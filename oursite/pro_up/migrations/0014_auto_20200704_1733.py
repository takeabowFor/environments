# Generated by Django 3.0.7 on 2020-07-04 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_up', '0013_auto_20200704_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='pro_info',
            name='sales',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pro_info',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]
