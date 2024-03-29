# Generated by Django 4.1.7 on 2024-02-01 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ride_sharing_app", "0017_alter_ride_driver"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ride",
            name="status",
            field=models.CharField(
                choices=[
                    ("requested", "Requested"),
                    ("started", "Started"),
                    ("completed", "Completed"),
                    ("cancelled", "Cancelled"),
                    ("accepted", "accepted"),
                ],
                default="requested",
                max_length=15,
            ),
        ),
    ]
