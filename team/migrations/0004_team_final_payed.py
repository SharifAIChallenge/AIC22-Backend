# Generated by Django 3.0.1 on 2022-08-25 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0003_auto_20220823_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='final_payed',
            field=models.BooleanField(default=False),
        ),
    ]
