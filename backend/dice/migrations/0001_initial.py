# Generated by Django 5.1.8 on 2025-05-02 19:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiceGameModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bet', models.IntegerField()),
                ('guessed_number', models.IntegerField()),
                ('choice1', models.CharField(max_length=2)),
                ('choice2', models.CharField(max_length=2)),
                ('roll1', models.IntegerField()),
                ('roll2', models.IntegerField()),
                ('total', models.IntegerField()),
                ('payout', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
