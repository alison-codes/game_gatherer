# Generated by Django 2.2 on 2019-06-12 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_played_won'),
    ]

    operations = [
        migrations.AlterField(
            model_name='played',
            name='won',
            field=models.CharField(choices=[('T', True), ('F', False)], default='T', max_length=1),
        ),
    ]