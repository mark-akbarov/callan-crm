# Generated by Django 4.2.3 on 2024-02-04 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_enrollment'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='knowledge_level',
            field=models.CharField(default='beginner', max_length=255),
            preserve_default=False,
        ),
    ]