# Generated by Django 4.0.5 on 2022-06-21 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('healthpizza', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food_nutr_content',
            old_name='content_per_gram',
            new_name='content_per_100_gram',
        ),
    ]
