# Generated by Django 2.2 on 2019-06-12 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20190611_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='played',
            name='date',
            field=models.DateField(verbose_name='played date'),
        ),
        migrations.AlterField(
            model_name='played',
            name='won',
            field=models.BooleanField(default=True),
        ),
    ]
