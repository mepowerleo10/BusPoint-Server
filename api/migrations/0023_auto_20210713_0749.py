# Generated by Django 3.2.4 on 2021-07-13 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20210713_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stop',
            name='lat',
            field=models.CharField(max_length=11),
        ),
        migrations.AlterField(
            model_name='stop',
            name='lon',
            field=models.CharField(max_length=11),
        ),
    ]
