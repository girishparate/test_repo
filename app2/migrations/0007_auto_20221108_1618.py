# Generated by Django 3.2.2 on 2022-11-08 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0006_attendance_present'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='absent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='attendance',
            name='half_day',
            field=models.BooleanField(default=False),
        ),
    ]
