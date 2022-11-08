# Generated by Django 4.1.3 on 2022-11-08 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('choice', '0005_alter_player_bb_alter_player_dp_alter_player_hr_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('four', models.FloatField()),
                ('six', models.FloatField()),
                ('eight', models.FloatField()),
                ('ten', models.FloatField()),
                ('CI', models.FloatField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preference', to='choice.subject')),
            ],
        ),
    ]
