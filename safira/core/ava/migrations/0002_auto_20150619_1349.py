# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ava', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='chave_expira',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 19, 13, 49, 6, 454601), blank=True),
            preserve_default=True,
        ),
    ]
