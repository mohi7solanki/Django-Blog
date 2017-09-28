# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 13:37
from __future__ import unicode_literals

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20170924_0726'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-timestamp', '-updated']},
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=tinymce.models.HTMLField(verbose_name='Content'),
        ),
    ]