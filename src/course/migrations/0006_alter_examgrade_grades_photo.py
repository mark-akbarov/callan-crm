# Generated by Django 4.2.3 on 2024-03-06 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_alter_category_options_course_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examgrade',
            name='grades_photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
