# Generated by Django 2.2.3 on 2019-08-04 00:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0022_auto_20190803_1906'),
    ]

    operations = [
        migrations.RenameField(
            model_name='annotation',
            old_name='community_annotation',
            new_name='annotation_community',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='community_user',
            new_name='user_community',
        ),
    ]
