# Generated by Django 3.2.4 on 2021-07-11 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_journey_route'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journey',
            name='route',
        ),
    ]