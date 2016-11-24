# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ava', '0004_auto_20150622_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='chave_expira',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 22, 10, 43, 20, 742754), blank=True),
            preserve_default=True,
        ),
    ]
