# Generated by Django 3.2.2 on 2021-07-16 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apex', '0028_auto_20210621_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='rawmaterial',
            name='Vendor',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='To',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
