# Generated by Django 3.0.1 on 2022-07-06 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0020_utmtracker_sign_up_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistic',
            name='model',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
