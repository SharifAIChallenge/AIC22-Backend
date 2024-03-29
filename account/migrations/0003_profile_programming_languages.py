# Generated by Django 3.0.1 on 2022-06-04 17:06

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='programming_languages',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Java', 'JAVA'), ('Python 3', 'PYTHON3'), ('C++', 'CPP')], default=None, max_length=17),
        ),
    ]
