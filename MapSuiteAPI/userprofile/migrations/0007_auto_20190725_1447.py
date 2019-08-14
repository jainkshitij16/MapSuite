# Generated by Django 2.2.3 on 2019-07-25 21:47

from django.db import migrations, models
import django.utils.timezone
import userprofile.validators


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_auto_20190725_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annotation',
            name='ann_date_time',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='The date and time this annotation holds importance for you', validators=[userprofile.validators.datevalidator]),
        ),
    ]
