# Generated by Django 5.0.6 on 2024-07-06 06:41
from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_post_tags"),
    ]

    operations = [
        TrigramExtension(),
    ]
