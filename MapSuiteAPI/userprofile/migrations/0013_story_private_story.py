# Generated by Django 2.2.3 on 2019-08-01 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0012_auto_20190801_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='private_story',
            field=models.BooleanField(default=False, help_text='Is the story private or not'),
        ),
    ]
