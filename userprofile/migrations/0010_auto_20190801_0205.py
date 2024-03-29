# Generated by Django 2.2.3 on 2019-08-01 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0009_auto_20190731_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('community_name', models.CharField(help_text='The name of the community the users belong to', max_length=30, unique=True)),
                ('private_community', models.BooleanField(default=False)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='groupby',
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_name', models.CharField(help_text='The name of the story', max_length=30, unique=True)),
                ('story_owner', models.ForeignKey(help_text='the owner of the story', on_delete=django.db.models.deletion.CASCADE, to='userprofile.Userprofile')),
            ],
        ),
    ]
