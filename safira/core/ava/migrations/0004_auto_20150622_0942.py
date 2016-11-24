# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ava', '0003_auto_20150619_1704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='chave_expira',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 22, 9, 42, 21, 551445), blank=True),
            preserve_default=True,
        ),
    ]
