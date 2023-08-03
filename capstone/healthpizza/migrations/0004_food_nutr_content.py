# Generated by Django 4.0.5 on 2022-06-21 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('healthpizza', '0003_delete_food_nutr_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food_Nutr_content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_per_100_gram', models.FloatField()),
                ('unit_of_measurement', models.CharField(max_length=10)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food', to='healthpizza.food')),
                ('nutrient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nutrient', to='healthpizza.nutrient')),
            ],
        ),
    ]