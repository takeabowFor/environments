# Generated by Django 3.0.7 on 2020-06-28 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_up', '0009_auto_20200628_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pro_info',
            name='p_picture',
            field=models.ImageField(default='', upload_to='pro_up/static/<django.db.models.fields.related.ForeignKey>/'),
        ),
    ]
