# Generated by Django 3.0.7 on 2020-06-27 02:23

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sup_med', '0004_sup_info_logo'),
        ('pro_up', '0002_pro_info_pro_token'),
        ('user_md', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_info',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('uname', models.CharField(max_length=128)),
                ('upassword', models.CharField(max_length=32)),
                ('ID_num', models.CharField(max_length=32, null=True)),
                ('BC_num', models.CharField(max_length=32, null=True)),
                ('uphone', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='User_token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64, verbose_name='用户token')),
                ('expiration_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='过期时间')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='user_md.User_info')),
            ],
        ),
        migrations.CreateModel(
            name='Records',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stime', models.DateTimeField(default=datetime.datetime.now, verbose_name='浏览时间')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pro_up.Pro_info')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sup_med.Sup_info')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_md.User_info')),
            ],
        ),
        migrations.CreateModel(
            name='Receiveinfo',
            fields=[
                ('rid', models.AutoField(primary_key=True, serialize=False)),
                ('rname', models.CharField(max_length=64)),
                ('raddress', models.CharField(max_length=256)),
                ('rphone', models.CharField(max_length=32)),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_md.User_info')),
            ],
        ),
        migrations.CreateModel(
            name='Likestores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sup_med.Sup_info')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_md.User_info')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('psum', models.IntegerField()),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pro_up.Pro_info')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_md.User_info')),
            ],
        ),
    ]
