# Generated by Django 3.0.7 on 2020-07-07 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sup_med', '0007_auto_20200704_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='sup_info',
            name='sstate',
            field=models.CharField(default='待审核', max_length=50),
        ),
    ]
