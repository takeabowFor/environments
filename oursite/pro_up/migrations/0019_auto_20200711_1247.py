# Generated by Django 3.0.7 on 2020-07-11 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pro_up', '0018_auto_20200709_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pro_info',
            name='address',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='pro_info',
            name='category',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='pro_info',
            name='para',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='pro_info',
            name='pkeyword',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='pro_info',
            name='pname',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='pro_info',
            name='problems',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='pro_info',
            name='psize',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='pro_info',
            name='ptype',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='pro_info',
            name='pusage',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='pro_info',
            name='symptoms',
            field=models.CharField(max_length=256),
        ),
    ]
