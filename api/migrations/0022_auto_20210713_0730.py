# Generated by Django 3.2.4 on 2021-07-13 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_stopinfo_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stop',
            name='lat',
            field=models.DecimalField(decimal_places=8, max_digits=12),
        ),
        migrations.AlterField(
            model_name='stop',
            name='lon',
            field=models.DecimalField(decimal_places=8, max_digits=12),
        ),
    ]
