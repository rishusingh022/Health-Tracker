# Generated by Django 3.0.8 on 2020-12-27 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthtracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='Gender',
            field=models.CharField(max_length=6),
        ),
    ]
