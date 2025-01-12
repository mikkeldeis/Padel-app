# Generated by Django 5.1.4 on 2025-01-08 09:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='match_type',
        ),
        migrations.RemoveField(
            model_name='match',
            name='player1',
        ),
        migrations.RemoveField(
            model_name='match',
            name='player1_score',
        ),
        migrations.RemoveField(
            model_name='match',
            name='player2',
        ),
        migrations.RemoveField(
            model_name='match',
            name='player2_score',
        ),
        migrations.RemoveField(
            model_name='match',
            name='player3',
        ),
        migrations.RemoveField(
            model_name='match',
            name='player3_score',
        ),
        migrations.RemoveField(
            model_name='match',
            name='player4',
        ),
        migrations.RemoveField(
            model_name='match',
            name='player4_score',
        ),
        migrations.AddField(
            model_name='match',
            name='score',
            field=models.CharField(default='0-0', max_length=100),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wins', models.IntegerField(default=0)),
                ('losses', models.IntegerField(default=0)),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_player1', to=settings.AUTH_USER_MODEL)),
                ('player2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_player2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='team1',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='match_team1', to='api.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team2',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='match_team2', to='api.team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='loser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_loser', to='api.team'),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_winner', to='api.team'),
        ),
    ]
