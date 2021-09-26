# Generated by Django 3.1.12 on 2021-09-26 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(default='default_pp.png', upload_to='profile_pictures', verbose_name='picture')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='', max_length=2)),
                ('bio', models.CharField(blank=True, max_length=500)),
                ('date_of_birth', models.DateTimeField(blank=True, null=True, verbose_name='date of birth')),
                ('following', models.ManyToManyField(blank=True, related_name='followers', to='profiles.Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
