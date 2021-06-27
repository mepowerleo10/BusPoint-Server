# Generated by Django 3.2.4 on 2021-06-26 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_journey_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='end_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end_point', to='api.stop'),
        ),
        migrations.AlterField(
            model_name='route',
            name='start_point',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start_point', to='api.stop'),
        ),
    ]
