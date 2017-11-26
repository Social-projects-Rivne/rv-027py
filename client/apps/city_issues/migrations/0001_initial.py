# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-22 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
                ('alias', models.TextField(blank=True, null=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('hashed_password', models.TextField(blank=True, max_length=256, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('delete_date', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.TextField()),
            ],
            options={
                'db_table': 'roles',
                'managed': False,
            },
        ),
    ]
