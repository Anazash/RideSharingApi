# Generated by Django 4.1.7 on 2024-01-30 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ride_sharing_app", "0003_alter_ride_driver_alter_ride_rider_userprofile"),
    ]

    operations = [
        migrations.RemoveField(model_name="userprofile", name="is_driver",),
        migrations.RemoveField(model_name="userprofile", name="is_rider",),
        migrations.AddField(
            model_name="userprofile",
            name="user_type",
            field=models.CharField(
                choices=[("rider", "Rider"), ("driver", "Driver")],
                default=1,
                max_length=10,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="ride",
            name="rider",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rides_as_rider",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="ride",
            name="status",
            field=models.CharField(
                choices=[
                    ("requested", "Requested"),
                    ("started", "Started"),
                    ("completed", "Completed"),
                    ("cancelled", "Cancelled"),
                ],
                default="requested",
                max_length=15,
            ),
        ),
    ]
