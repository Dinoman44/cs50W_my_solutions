from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Nutr_type)
admin.site.register(Nutrient)
admin.site.register(Food)
admin.site.register(Food_Nutr_content)
admin.site.register(Disease)
admin.site.register(User_Requested_Additions)