# Generated by Django 2.2.3 on 2019-07-19 23:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Userprofile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_bio', models.CharField(max_length=180)),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(default='location name', max_length=30)),
                ('latitude', models.DecimalField(decimal_places=4, default=49.2642, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=4, default=123.2532, max_digits=10)),
                ('ann_text', models.CharField(max_length=250)),
                ('ann_date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_user', to='userprofile.Userprofile')),
            ],
        ),
    ]
