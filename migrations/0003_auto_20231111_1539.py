# Generated by Django 3.2.16 on 2023-11-11 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nextgis_common', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthState',
            fields=[
                ('value', models.TextField(primary_key=True, serialize=False)),
                ('client_id', models.TextField(blank=True, db_index=True, default=None, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
        migrations.AddField(
            model_name='accesstoken',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='oauth_state', to='nextgis_common.oauthstate'),
        ),
    ]