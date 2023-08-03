from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import CharField, FloatField, BooleanField
from django.db.models.fields.related import ForeignKey

# Create your models here.

class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"
    pass


class Nutr_type(models.Model):
    name = CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

  
class Nutrient(models.Model):
    simple = CharField(max_length=50, default="vitD")
    name = CharField(max_length=50)
    type = ForeignKey(Nutr_type, on_delete=models.CASCADE, related_name="type of nutrient+")
    daily_min_intake = FloatField()
    daily_max_intake = FloatField()
    unit_of_measurement = CharField(max_length=10)

    def __str__(self):
        return f"{self.name}, {self.type}. DRI: {self.daily_min_intake} to {self.daily_max_intake} {self.unit_of_measurement}"


class Disease(models.Model):
    simple = CharField(max_length=50, default="goitre")
    name = CharField(max_length=50)
    relevant_nutrient = ForeignKey(Nutrient, on_delete=models.CASCADE, related_name="relevant nutrient+")

    def __str__(self):
        return f"{self.name}, caused by deficiency/excess of {self.relevant_nutrient}"


class Food(models.Model):
    simple = CharField(max_length=50, default="cheese")
    name = CharField(max_length=100)
    is_veg = BooleanField()
    allergen_type = CharField(max_length=50)
    type = CharField(max_length=50, default="cheese")

    def __str__(self):
        return f"{self.name} | is veg? {self.is_veg} | allergens? {self.allergen_type} | "
    


class Food_Nutr_content(models.Model):
    food = ForeignKey(Food, on_delete=models.CASCADE, related_name="food")
    nutrient = ForeignKey(Nutrient, on_delete=models.CASCADE, related_name="nutrient")
    content_per_100_gram = FloatField()
    unit_of_measurement = CharField(max_length=10)

    def __str__(self):
        return f"{self.food} has {self.nutrient} content of {self.content_per_100_gram} {self.unit_of_measurement}/100g"


class User_Requested_Additions(models.Model):
    requester = ForeignKey(User, on_delete=models.CASCADE, related_name="requester")
    requested_edit = CharField(max_length=40)
    edit_info = CharField(max_length=300)
    edit_type = CharField(max_length=10)

    def __str__(self):
        return f"{self.requester} requested to add {self.requested_edit} ({self.edit_info}), a {self.edit_type}"