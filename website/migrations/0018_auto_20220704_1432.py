# Generated by Django 3.0.1 on 2022-07-04 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_utmtracker'),
    ]

    operations = [
        migrations.RenameField(
            model_name='staff',
            old_name='url',
            new_name='github_url',
        ),
        migrations.AddField(
            model_name='staff',
            name='linkedin_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]