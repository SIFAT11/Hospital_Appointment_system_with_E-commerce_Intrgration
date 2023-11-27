# Generated by Django 4.2.5 on 2023-09-28 17:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment', '0004_remove_appointment_id_appointment_appointment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='Appointment_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]