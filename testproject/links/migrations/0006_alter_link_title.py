# Generated by Django 5.0.4 on 2024-04-21 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0005_collection_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
