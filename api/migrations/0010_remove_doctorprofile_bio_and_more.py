# Generated by Django 5.0.2 on 2024-02-27 12:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_rename_patient_id_patientprofile_patient_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="doctorprofile",
            name="bio",
        ),
        migrations.RemoveField(
            model_name="doctorprofile",
            name="doctor_id",
        ),
        migrations.RemoveField(
            model_name="doctorprofile",
            name="image",
        ),
        migrations.RemoveField(
            model_name="doctorprofile",
            name="rating",
        ),
        migrations.RemoveField(
            model_name="doctorprofile",
            name="verified",
        ),
        migrations.RemoveField(
            model_name="patientprofile",
            name="city",
        ),
        migrations.RemoveField(
            model_name="patientprofile",
            name="gender",
        ),
        migrations.RemoveField(
            model_name="patientprofile",
            name="government",
        ),
        migrations.RemoveField(
            model_name="patientprofile",
            name="image",
        ),
        migrations.RemoveField(
            model_name="patientprofile",
            name="patient_id",
        ),
        migrations.RemoveField(
            model_name="patientprofile",
            name="phone_number",
        ),
        migrations.AlterField(
            model_name="doctorprofile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="api.doctor"
            ),
        ),
        migrations.AlterField(
            model_name="patientprofile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="api.patient"
            ),
        ),
    ]