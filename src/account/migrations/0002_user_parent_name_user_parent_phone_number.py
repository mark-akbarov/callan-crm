# Generated by Django 4.2.3 on 2024-02-03 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='parent_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='parent_phone_number',
            field=models.CharField(max_length=25, null=True, unique=True),
        ),
    ]
