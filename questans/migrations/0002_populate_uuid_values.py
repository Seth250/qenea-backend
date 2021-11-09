# Generated by Django 3.1.12 on 2021-11-04 09:33

import uuid

from django.db import migrations


def gen_uuid(apps, schema_editor):
    Question = apps.get_model('questans', 'Question')
    for row in Question.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=['uuid'])


class Migration(migrations.Migration):

    dependencies = [
        ('questans', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(gen_uuid)
    ]