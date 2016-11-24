# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ava', '0002_auto_20150619_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='chave_expira',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 19, 17, 4, 1, 373028), blank=True),
            preserve_default=True,
        ),
    ]
