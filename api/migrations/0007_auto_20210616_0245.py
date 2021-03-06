# Generated by Django 3.2.4 on 2021-06-16 02:45

from django.db import migrations
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20210616_0159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stopnotifyorder',
            name='Journey',
        ),
        migrations.RemoveField(
            model_name='stopnotifyorder',
            name='stop',
        ),
        migrations.RemoveField(
            model_name='journey',
            name='notify_stops',
        ),
        migrations.AddField(
            model_name='journey',
            name='notify_stops',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='notify_stops', to='api.Stop'),
        ),
        migrations.RemoveField(
            model_name='journey',
            name='routes',
        ),
        migrations.AddField(
            model_name='journey',
            name='routes',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='routes', to='api.Route'),
        ),
        migrations.DeleteModel(
            name='RouteOrder',
        ),
        migrations.DeleteModel(
            name='StopNotifyOrder',
        ),
    ]
