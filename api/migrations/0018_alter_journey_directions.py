# Generated by Django 3.2.4 on 2021-07-11 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_rename_route_journey_directions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journey',
            name='directions',
            field=models.JSONField(default=''),
        ),
    ]
