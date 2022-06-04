# Generated by Django 3.0.1 on 2022-06-04 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleLogin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=1024)),
                ('expires_at', models.PositiveIntegerField()),
                ('expires_in', models.PositiveIntegerField()),
                ('id_token', models.TextField()),
                ('scope', models.TextField()),
                ('is_signup', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
    ]
