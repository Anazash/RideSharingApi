# Generated by Django 4.1.7 on 2024-01-31 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ride_sharing_app", "0006_userprofile_dob_alter_userprofile_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="user",
            field=models.CharField(max_length=255),
        ),
    ]