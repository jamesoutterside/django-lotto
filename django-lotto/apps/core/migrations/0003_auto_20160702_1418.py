# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-02 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160702_1238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name_plural': 'Entries'},
        ),
        migrations.AlterModelOptions(
            name='lottery',
            options={'ordering': ('date_created',), 'verbose_name_plural': 'Lotteries'},
        ),
        migrations.AddField(
            model_name='lottery',
            name='prize',
            field=models.CharField(default=b'Car', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lottery',
            name='draw_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lottery',
            name='draw_result',
            field=models.CommaSeparatedIntegerField(blank=True, max_length=255, null=True),
        ),
    ]
