# Generated by Django 4.1.7 on 2024-01-31 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ride_sharing_app", "0008_userprofile_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="confirm_password",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="userprofile",
            name="password",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
