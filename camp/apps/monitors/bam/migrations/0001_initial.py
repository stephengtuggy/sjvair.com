# Generated by Django 3.0.6 on 2020-06-24 08:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('monitors', '0003_auto_20200604_0016'),
    ]

    operations = [
        migrations.CreateModel(
            name='BAM1022',
            fields=[
                ('monitor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='monitors.Monitor')),
                ('auth_key', models.UUIDField(default=uuid.uuid4)),
            ],
            bases=('monitors.monitor',),
        ),
    ]
