# Generated by Django 5.1.4 on 2025-01-15 13:50

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_date_match_played_at_remove_match_loser_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='played_at',
        ),
        migrations.RemoveField(
            model_name='match',
            name='team1',
        ),
        migrations.RemoveField(
            model_name='match',
            name='team1_score',
        ),
        migrations.RemoveField(
            model_name='match',
            name='team1_set_scores',
        ),
        migrations.RemoveField(
            model_name='match',
            name='team2',
        ),
        migrations.RemoveField(
            model_name='match',
            name='team2_score',
        ),
        migrations.RemoveField(
            model_name='match',
            name='team2_set_scores',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='date',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='matches',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='teams',
        ),
        migrations.AddField(
            model_name='match',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='score_team_1',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='match',
            name='score_team_2',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='match',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending', max_length=15),
        ),
        migrations.AddField(
            model_name='match',
            name='team_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_1_matches', to='api.team'),
        ),
        migrations.AddField(
            model_name='match',
            name='team_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_2_matches', to='api.team'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tournament',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won_matches', to='api.team'),
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', models.IntegerField()),
                ('start_date', models.DateField()),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.tournament')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='round',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='api.round'),
        ),
    ]
