# Generated by Django 4.2.5 on 2023-09-28 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0002_doctor'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Alevel', models.CharField(max_length=100)),
                ('higher_educations', models.CharField(max_length=100)),
                ('qualifications', models.CharField(max_length=100)),
                ('appointment', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('appointment_times', models.ManyToManyField(to='Doctor.appointmenttime')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.department')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor')),
            ],
        ),
    ]
