# Generated by Django 3.1.7 on 2021-03-13 07:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('moviespy', '0002_funcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcion',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2021, 3, 13, 7, 12, 40, 910379, tzinfo=utc)),
        ),
    ]
