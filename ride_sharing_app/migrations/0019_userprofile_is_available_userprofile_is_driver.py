# Generated by Django 4.1.7 on 2024-02-01 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ride_sharing_app", "0018_alter_ride_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="is_available",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="is_driver",
            field=models.BooleanField(default=False),
        ),
    ]