# Generated by Django 4.2.5 on 2023-09-28 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment', '0005_alter_appointment_appointment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='gender',
            field=models.CharField(choices=[('other', 'Other'), ('male', 'Male'), ('female', 'Female')], max_length=10),
        ),
    ]