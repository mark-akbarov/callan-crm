# Generated by Django 4.2.3 on 2024-03-03 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_enrollment_knowledge_level_alter_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='knowledge_level',
            field=models.CharField(choices=[("Boshlang'ich", 'Beginner'), ("O'rta", 'Elementary'), ('Yuqori', 'Intermediate')], max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('Admin', 'Admin'), ("O'qituvchi", 'Teacher'), ("O'quvchi", 'Student')], max_length=15),
        ),
    ]
