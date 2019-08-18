# Generated by Django 2.2.3 on 2019-08-02 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0018_auto_20190801_2343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annotation',
            name='story',
        ),
        migrations.RemoveField(
            model_name='annotation',
            name='story_privacy',
        ),
        migrations.AddField(
            model_name='annotation',
            name='annotation_privacy',
            field=models.BooleanField(default=False, help_text='Is the annotation private or not'),
        ),
    ]