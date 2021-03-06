# Generated by Django 3.2.2 on 2021-05-26 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apex', '0018_alter_rawmaterial_rm_grade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deleted_tables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_id', models.CharField(blank=True, max_length=40, null=True)),
                ('material_id', models.CharField(blank=True, max_length=40, null=True)),
                ('quantity', models.CharField(blank=True, max_length=40, null=True)),
                ('size', models.CharField(blank=True, max_length=40, null=True)),
                ('type', models.CharField(blank=True, max_length=40, null=True)),
                ('weight', models.CharField(blank=True, max_length=40, null=True)),
                ('date', models.CharField(blank=True, max_length=40, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='rawmaterial',
            name='RM_Grade',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
