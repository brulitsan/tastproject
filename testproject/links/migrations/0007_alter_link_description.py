# Generated by Django 5.0.4 on 2024-04-21 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0006_alter_link_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
