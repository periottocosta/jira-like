# Generated by Django 4.2.13 on 2024-06-27 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('team_name', models.CharField(default='PERIOTTO-TEAM', max_length=255)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.clients')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'ordering': ['created_at'],
            },
        ),
    ]
