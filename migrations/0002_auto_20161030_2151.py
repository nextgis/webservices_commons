# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-30 21:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nextgis_common', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accesstoken',
            old_name='expires_in',
            new_name='expires_at',
        ),
        migrations.AlterIndexTogether(
            name='accesstoken',
            index_together=set([('user', 'access_token')]),
        ),
    ]