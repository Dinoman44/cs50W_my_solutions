from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from .util import get_entry, map_allergies
from markdown import markdown

from .models import *

# default view
def index(request):
    return render(request, "healthpizza/index.html")


# login view
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "healthpizza/login.html")


# logout view
@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return redirect(reverse("index"))


# registration view
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "healthpizza/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect(reverse("index"))
    else:
        return render(request, "healthpizza/register.html")


# view to look at list of diseases
@login_required(login_url="/login")
def disease_list(request):
    # get all diseases and send it back
    diseases = Disease.objects.all().order_by("name")
    return render(request, "healthpizza/diseases.html", {
        "diseases": diseases
    })


# view to look at list of nutrients
@login_required(login_url="/login")
def nutrient_list(request):
    # get all nutrients and send it back
    nutrients = Nutrient.objects.all().order_by("name")
    return render(request, "healthpizza/nutrients.html", {
        "nutrients": nutrients
    })


# view to look at list of foods
@login_required(login_url="/login")
def food_list(request):
    foods = Food.objects.all().order_by("name")
    foods_with_nutr = []
    for food in foods:
        item = [food, Food_Nutr_content.objects.filter(food=food)]
        foods_with_nutr.append(item)
    return render(request, "healthpizza/food_list.html", {
        "foods": foods_with_nutr
    })


# view to look at info on a disease
@login_required(login_url="/login")
def disease_info(request, disease_ID):
    if request.method == "POST":
        nutr = request.POST.get("nutrient")
        disease_info.nutrient = nutr
        return redirect(reverse("pizza prefs"))

    # first use the name of the disease to get its db entry
    disease = Disease.objects.filter(simple=disease_ID.lower()).first()
    if disease:
        # if the disease exists, get its wiki-style markdown page
        text = get_entry("disease", disease.simple)

        if text:
            # if the page exists, convert it to html and render it in the page
            final_text = markdown(text)
            disease_info.disease = disease

            return render(request, "healthpizza/disease_info.html", { 
                "disease_details": final_text,
                "disease": disease,
                "mistake": False
            })
    
    # if the disease is not present in the db, or its page does not exist, return a 404 page
    return render(request, "healthpizza/disease_info.html", {
        "mistake": True,
        "requested_name": disease_ID
    })


# view to look at info on a nutrient
@login_required(login_url="/login")
def nutrient_info(request, nutrient_ID):
    if request.method == "POST":
        nutr = request.POST.get("nutrient")
        disease_info.nutrient = nutr
        nutr_simple = Nutrient.objects.filter(simple=nutr).first()
        disease_info.disease = Disease.objects.filter(relevant_nutrient=nutr_simple).first()
        return redirect(reverse("pizza prefs"))
    
    # first use the name of the nutrient to get its db entry
    nutrient = Nutrient.objects.filter(simple=nutrient_ID.lower()).first()
    if nutrient:
        # if the nutrient exists, get its wiki-style markdown page
        text = get_entry("nutrient", nutrient.simple)

        if text:
            # if the page exists, convert it to html and render it in the page
            final_text = markdown(text)

            return render(request, "healthpizza/nutrient_info.html", {
                "nutrient_details": final_text,
                "nutrient": nutrient,
                "mistake": False
            })

    # if the nutrient is not present in the db, or its page does not exist, return a 404 page
    return render(request, "healthpizza/nutrient_info.html", {
        "mistake": True,
        "requested_name": nutrient_ID
    })


# view to select pizza preferences
@login_required(login_url="/login")
def pizza_prefs(request):
    if request.method == "GET":
        if disease_info.nutrient:
            return render(request, "healthpizza/pizza_prefs.html", {"nutrient": disease_info.nutrient})
        else:
            return render(request, "healthpizza/pizza_prefs.html", {"nutrient": nutrient_info.nutrient})
    
    isveg = request.POST.get("isveg").lower()
    if isveg == "true":
        isveg = True
    else:
        isveg = False
    allergies_0 = request.POST.get("allergies").split()
    pizza_prefs.nutrient = Nutrient.objects.filter(simple=request.POST.get("nutrient").lower()).first()
    allergies = map_allergies(allergies_0)
    if not isveg:
        possible_foods = Food.objects.all()
        if allergies != "none":
            foods = []
            for option in possible_foods:
                if option.allergen_type not in allergies:
                    foods.append(option)
        else:
            foods = possible_foods
    else:
        possible_foods = Food.objects.filter(is_veg=True)
        if allergies != "none":
            foods = []
            for option in possible_foods:
                if option.allergen_type not in allergies:
                    foods.append(option)
        else:
            foods = possible_foods

    foods_with_req_nutrient = []
    for food in foods:
        if Food_Nutr_content.objects.filter(food=food, nutrient=pizza_prefs.nutrient).exists():
            foods_with_req_nutrient.append(food)
    
    pizza_prefs.foods = foods_with_req_nutrient
    return redirect(reverse("pizza gen"))


# view to generate and return a pizza
@login_required(login_url="/login")
def generate_pizza(request):
    # get global vars with disease, nutrient and food list
    disease = disease_info.disease
    nutrient = pizza_prefs.nutrient
    foods = pizza_prefs.foods
    toppings_list1 = []
    toppings_list = []

    for food in foods:
        if food.type == "cheese" or food.type == "veg" or food.type == "mushrooms":
            nutr_content = Food_Nutr_content.objects.filter(food=food, nutrient=nutrient).first()
            nutr_amt = round(1.2 * nutr_content.content_per_100_gram)
            toppings_list1.append(tuple((food, 120, nutr_amt, nutr_content.unit_of_measurement)))
        if food.type == "meat" or food.type == "fish":
            nutr_content = Food_Nutr_content.objects.filter(food=food, nutrient=nutrient).first()
            nutr_amt = round(nutr_content.content_per_100_gram)
            toppings_list1.append(tuple((food, 100, nutr_amt, nutr_content.unit_of_measurement)))
        if food.type == "dressing":
            nutr_content = Food_Nutr_content.objects.filter(food=food, nutrient=nutrient).first()
            nutr_amt = round(0.2 * nutr_content.content_per_100_gram)
            toppings_list1.append(tuple((food, 20, nutr_amt, nutr_content.unit_of_measurement)))
        
    # find highest of each food category
    high_c = (0,0,0,0,)
    high_v = (0,0,0,0,)
    high_mt = (0,0,0,0,)
    high_mr = (0,0,0,0,)
    high_f = (0,0,0,0,)
    thingy1 = []
    for topping in toppings_list1:
        if topping[0].type == "cheese":
            if high_c[2] < topping[2]:
                high_c = topping
        elif topping[0].type == "meat":
            if high_mt[2] < topping[2]:
                high_mt = topping
        elif topping[0].type == "fish":
            if high_f[2] < topping[2]:
                high_f = topping
        elif topping[0].type == "mushrooms":
            if high_mr[2] < topping[2]:
                high_mr = topping
        elif topping[0].type == "veg":
            if high_v[2] < topping[2]:
                high_v = topping
        elif topping[0].type == "dressing":
            thingy1.append(topping)
    
    # remove unavailable categories
    thingy1 += [high_c, high_mt, high_v, high_f, high_mr]
    thingy = []
    for thing in thingy1:
        if thing != (0,0,0,0,):
            thingy.append(thing)

    # get list of alternative toppings
    for topping in toppings_list1:
        if topping not in thingy:
            toppings_list.append(topping)

    amt_of_nutr = 0
    for l in thingy:
        amt_of_nutr += l[2]

    # find % of DRI
    percentage_intake = f"{round((amt_of_nutr/nutrient.daily_max_intake)*100)} to {round((amt_of_nutr/nutrient.daily_min_intake)*100)}"
    if round((amt_of_nutr/nutrient.daily_max_intake)*100) > 110:
        warning = "You might want to reduce the quantity of one or more of the toppings"
        return render(request, "healthpizza/pizza.html", {
            "nutrient": nutrient,
            "foods": foods,
            "disease": disease,
            "toppings": toppings_list,
            "best_toppings": thingy,
            "total_nutr": amt_of_nutr,
            "percentage_intake": percentage_intake,
            "warning": warning
        })
    
    return render(request, "healthpizza/pizza.html", {
        "nutrient": nutrient,
        "foods": foods,
        "disease": disease,
        "toppings": toppings_list,
        "best_toppings": thingy,
        "total_nutr": amt_of_nutr,
        "percentage_intake": percentage_intake,
        "warning": False
    })


# view to store user's requested information
@login_required(login_url="/login")
def request_info(request):
    if request.method == "GET":
        return render(request, "healthpizza/request_info.html")

    edit_name = request.POST.get("edit name")
    description = request.POST.get("descr")
    type = request.POST.get("type")
    new_requested_edit = User_Requested_Additions.objects.create(requester=request.user, requested_edit=edit_name, edit_info=description, edit_type=type)
    new_requested_edit.save()

    return render(request, "healthpizza/request_info.html", {
        "message": "Request sent."
    })