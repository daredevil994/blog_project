# Generated by Django 2.1.7 on 2019-04-21 13:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190421_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 21, 13, 43, 34, 98958, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 21, 13, 43, 34, 97957, tzinfo=utc)),
        ),
    ]
