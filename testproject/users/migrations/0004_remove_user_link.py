# Generated by Django 5.0.4 on 2024-04-18 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='link',
        ),
    ]
