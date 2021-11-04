# Generated by Django 3.1.12 on 2021-11-04 09:34

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questans', '0002_populate_uuid_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]