# Generated by Django 2.2.3 on 2019-08-01 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0016_auto_20190801_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='story',
            field=models.CharField(help_text='The story name for the group of annotations', max_length=50, null=True),
        ),
    ]