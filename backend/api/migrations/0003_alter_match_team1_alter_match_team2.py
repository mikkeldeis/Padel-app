# Generated by Django 5.1.4 on 2025-01-08 09:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_match_match_type_remove_match_player1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='team1',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='match_team1', to='api.team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='team2',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='match_team2', to='api.team'),
        ),
    ]
