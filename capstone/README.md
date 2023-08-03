# Nutri-Pizza
### You are what you eat
Throughout the world, as diets become dominated with oily or sugary foods and fast food, 
essential nutrients including vitamins and minerals are decreasingly consumed.
These nutrients perform critical functions throughout the body, from improving eyesight to 
keeping the immune system healthy.

### The problem
Diseases and disorders caused due to improper diets are becoming more frequent across the world,
and especially in children. These problems range from obesity and diabetes due to overconsumption 
of sugar to more severe cases of stunted growth or underdevelopment of the eyes.
The majority of these problems can be prevented if we have proper balanced diets with good amounts
of vitamins and minerals. So why don't we? Well, people find pizzas and hamburgers to be 
more appetizing than vegetable soups and salads.

### The solution
If people like pizzas so much, why not make them healthier? My app can provide a list of toppings
that can be added to a pizza and provide a particular nutrient! And the toppings will be filtered
based on your dietary preferences too. The idea is to suggest people to look for pizzas with 
such toppings. Or better yet, make such a pizza yourself as a healthier option! 
Fast food places add lots of oil and use flour with greater amounts of carbohydrates, 
and you usually can't choose the exact toppings and amounts.


## Features
### `/disorder-list`
Gives a list of nutrition-related disorders available in the database.

### `/disorder/<disorder>`
Gives detailed information on the specific disorder being requested.

### `/nutrient-list`
Gives a list of nutrients available in the database.

### `/nutrient/<nutrient>`
Gives detailed information on the specific nutrient being requested.

### `/food-list`
Gives a list of foods available in the database.

### `/request_info`
If a user wants something to be added to our database, they can make a request at this route.

### `/pizza-prefs`
This route cannot be visited out of context; a user is redirected here from a page on a disorder/nutrient to select their dietary preferences for a pizza.

### `/pizza-gen`
This route cannot be visited out of context; a user is redirected here to be shown the toppings for a pizza that conforms to their dietary preferences and contains a nutrient that helps with a particular disorder.


## File contents
### `/detailed_entries`
This directory contains markdown files of entries on various nutrition-related disorders and nutrients.
 * `/detailed_entries/disease` contains the files for the diseases available in the database
 * `/detailed_entries/nutrient` contains the files for the nutrients available in the database

### `/healthpizza/static/healthpizza`
Contains the static files (CSS, JS and favicon) needed for the web app.
 * `/healthpizza/static/healthpizza/favicon.ico` is the favicon for the web app (the icon that appears in the corner of the browser tab)
 * `/healthpizza/static/healthpizza/logo.png` is the website logo, found in the navbar

#### `/healthpizza/static/healthpizza/styles.css`
This file contains all the CSS for the website elements. It is split into a number of sections:
 * The first section contains some general styling to be used throughout the web app, for the background, text font and size, footer etc.
 * The second section contains the styling for the navbar, including the menu links, logo and name
 * The third section contains styling for the text on the homepage
 * The fourth section contains styling for the forms in the site, including textboxes and buttons
 * The fifth section contains styling for the cards in the `/disorder-list`, `/nutrient-list`, `/food-list`, `/disorder/<disorder>` and `nutrient/<nutrient>` routes
 * The 6th section contains styling for error text, when a particular disorder/nutrient that the user is searching for is not available in the database
 * The seventh section contains styling for the disclaimer, consent form and choice confirmation text and buttons in the `/pizza-prefs` route

#### `/healthpizza/static/healthpizza/responsiveness.css`
This file contains CSS media queries to make the app mobile responsive.
 * Navbar is resized and stacked below the logo when screen width is < 950px
 * Text on homepage takes up more of the screen at smaller widths
 * Footer text size decreases and the menu gets stacked with the source link at smaller widths
 * At larger screen widths the info cards are fixed at a 400px width
 * Other adjustments of font size, stacking of divs, flexboxes etc. are done at various screen sizes

#### `/healthpizza/static/healthpizza/js`
This directory contains the javascript files used for the web app
 * `/healthpizza/static/healthpizza/js/main.js` contains general JS for the web app. It adds an event listener to the logo and hides the mobile version of the navbar and footer when the page is loaded.
 * `/healthpizza/static/healthpizza/js/n-d-info.js` contains JS that works when there is an error with a nutrient/disorder not being found.
 * `/healthpizza/static/healthpizza/js/pizza-prefs/js` is used in the `/pizza-prefs` route to handle the forms on the page. It declares some important html elements that are needed, then adds event listeners to the buttons. The first "next" button shows the disclaimer, the next one shows the final choices, and the "confirm" button is to confirm the choices. I decided to list the user's dietary preferences and allergies, that they will pick in the first form, as a string that will be sent via a different form. This was done to ensure frontend validation and for easier backend processing.

#### `/healthpizza/templates/healthpizza/`
Contains the template files for the web app.
 * `/healthpizza/templates/healthpizza/disease_info.html` shows the detailed entry information on a particular disorder, as retrieved from the `/healthpizza/detailed_entries/disease` directory.
 * `/healthpizza/templates/healthpizza/diseases.html` shows a list of disorders, arranged in a flex row that can wrap, as available in the database. For each disorder, a link to its detailed entry, its database id, and the nturient relevant to it.
 * `/healthpizza/templates/healthpizza/food_list.html` shows a list of foods, arranged in a flex row as before, as available in the database. For each food, its type, allergen type, database id, and nutrient content information is shown.
 * `/healthpizza/templates/healthpizza/index.html` is the home page of the app.
 * `/healthpizza/templates/healthpizza/layout.html` is the layout file that includes the general js/css files, top navbar and footer.
 * `/healthpizza/templates/healthpizza/login.html` is the login page with the login form.
 * `/healthpizza/templates/healthpizza/nutrient_info.html` as with `disease_info.html`, this page shows the detailed entry information on a particular nutrient, as retrieved from the `healthpizza/detailed_entries/nutrient` directory.
 * `/healthpizza/templates/healthpizza/nutrients.html` shows a list of nutrients, arranged in a flex row as before, as available in the database. For each nutrient a link to its detailed entry is given, along with the database id.
 * `/healthpizza/templates/healthpizza/pizza_prefs.html` is the page where the user picks their dietary preferences and accepts the consent form after reading the disclaimer; each section is hidden before each previous part is completed to ensure that the user does not miss out on an important form. The js file `/healthpizza/static/healthpizza/js/pizza_prefs.js` is used here for the frontend validation and option matching.
 * `/healthpizza/templates/healthpizza/pizza.html` is the page where the list of toppings for the pizza is shown.
 * `/healthpizza/templates/healthpizza/register.html` is the registration page for first-time users.
 * `/healthpizza/templates/healthpizza/request_info.html` is the page with a form for the user to fill out to request the addition of a new food/disorder/nutrient to the database.


### App files (under `/healthpizza`)
 * `admin.py` is where the Django models were registered to show them on the admin page
 * `apps.py` is where the app is registered
 * `urls.py` is where the url routes are registered
 * Other files are detailed below.

#### `/healthpizza/models.py`
Contains all the models for the app
 * `User` - model for storing user info (username, email, password etc.)
 * `Nutr_type` - model for storing the type of nutrient
 * `Nutrient` - model for storing information on nutrient. Contains the following fields:
    - `simple`: simple name for the nutrient, acts as database ID
    - `name`: name of nutrient
    - `type`: type of nutrient, references the `Nutr_type` model
    - `daily_min_intake`: lower bound for the daily recommended intake value (DRI)
    - `daily_max_intake`: upper bound for the same
    - `unit_of_measurement`: the unit used to measure the quantity of the nutrient in a sample
 * `Disease` - model for storing info on disorders
    - `simple`: simple name for the disorder, acts as database ID
    - `name`: name of disorder
    - `relevant_nutrient`: the nutrient that affects the disorder, references the `Nutrient` model
 * `Food` - model for storing info on foods
    - `simple`: simple name for the food, acts as database ID
    - `name`: name of the food
    - `is_veg`: boolean field telling whether or not the food is vegetarian
    - `allergen_type`: the allergen that the food has (fish, dairy product etc.)
    - `type`: type of food (vegetable, fruit, fish etc.)
 * `Food_Nutr_content` - model for storing info on the nutrient contents of foods
    - `food`: the food item, references the `Food` model
    - `nutrient`: the nutrient in the food, references the `Nutrient` model
    - `content_per_100_gram`: the content of the nutrient in 100 grams of the food
    - `unit_of_measurement`: the unit of measurement for the nutrient content in the food
 * `User_Requested_Additions` - model for storing user-requested additions
    - `requester`: the user who requested the edit/addition, references the `User` model
    - `requested_edit`: the requested change (nutrient/food/disorder to be added)
    - `edit_info`: a short description of the nutrient/food/disorder
    - `edit_type`: what change is being requested (new nutrient or food or disorder)

#### `/healthpizza/util.py`
Contains two utility functions used in `views.py`.
 * `get_entry`: this function gets the markdown entry for a disorder or nutrient from the directory `/detailed_entries` using two arguments - the type (nutrient or disease) and the database ID of the item. If no entry exists for the requested nutrient/disorder, `None` is returned and an error page is displayed to the user asking them to check the spelling, as well as if they are searching in the right type (if request for a nutrient is made to the disorder path then there is an error).
 * `map_allergies`: this functions takes the reported allergies of the user from the form and maps it to the allergy values used in the database. This is done because the form submits multiple allergies as a string, which is split into a list and mapped to the correct name. So `"lactose fish spice"` maps to `["Dairy Product", "Fish Product", "Spice"]`. Takes the allergies string and the mapping as arguments; the mapping is predefined within the function declaration.

#### `healthpizza/views.py`
Contains the views for each route.
 * `index`: view for the homepage, renders `healthpizza/index.html`. Called by `/` route.
 * `login_view`: view for login page, renders `healthpizza/login.html` upon GET request and redirects to `index` after successful login. Called by `/login` route.
 * `logout_view`: view for logging out, redirects to `index` upon successful logout. Called by `/logout` route.
 * `register`: view for registration page, renders `healthpizza/register.html` upon GET request and redirects to `index` after successful registration. Called by `/register` route.
 * `disease_list`: view that retrieves list of diseases available in the database, renders `healthpizza/diseases.html`. Called by `/disorder-list` route.
 * `nutrient_list`: view that retrieves list of nutrients available in the database, renders `healthpizza/nutrients.html`. Called by `/nutrient-list` route.
 * `food_list`: view that retrieves list of foods available in the database, renders `healthpizza/food_list.html`. Called by `/food-list` route.
 * `disease_info`: view that takes the database ID of the disease and retrieves the database entry for the disease using the `get_entry` function, rendering `healthpizza/disease_info.html`. Called by `/disease/<str:disease_ID>` route where `disease_ID` is the database ID of the disorder. A button on the page, "Generate Pizza" can be clicked, which send a POST request to this view. The function will store the disease's relevant nutrient in a global variable and then redirect to `/pizza-prefs`.
 * `nutrient_info`: Similar to `disease_info`, except that it does it for a nutrient. Called by `/disease/<str:nutrient_ID>` where `nutrient_ID` is the database ID of the nutrient. Renders `healthpizza/nutrient_info.html`. Similar "Generate Pizza" button redirects to `/pizza-prefs` after setting global variable as before.
 * `pizza_prefs`: view that renders the preferences page `healthpizza/pizza_prefs.html` that allows the user to customize the toppings to suit their dietary preferences and allergies. Details on how this process works is explained [here](##How the pizza toppings are generated). The view function processes the requirements and creates a global variable with the possible toppings. This list contains foods that contain the given nutrient, and conform to the dietary preferences of the user (for instance if a user chooses the "veg" option and gives "lactose intolerance" as an allergy, then non-veg and dairy products with lactose are excluded). Once this list is made and declared, the function redirects to `/pizza-gen`.
 * `generate_pizza`: view function that takes the previously-declared global variables with the disorder, nutrient and list of foods, and filters the foods. A list of 6 foods is made, with the highest topping amount. Each food is of a different category (one dressing, one vegetable, one cheese, one meat, one mushroom and one fish), and each food holds the highest amount of the nutrient for its category. Some categories may be excluded due to the user's dietary preference (ex: meat and fish are excluded for veg options) or due to the nutrient not being present in any of the foods (ex: Iodine is not present in mushrooms or vegetables, only in seafood and iodised salt). The view function renders `healthpizza/pizza.html`, which displays the main choice toppings (from the list of 6) as well as some alternative toppings. The view function also calculates the quantity of the nutrient offered by each topping based on a pre-set weight of topping, and calculates the total amount of the nutrient present on the pizza, and the percentage of the DRI for the nutrient that it meets. Called by `/pizza-gen`.
 * `request_info`: view function that renders `healthpizza/request_info.html`. A GET request will display the page with the form for a user to request an addition to the database in the form of a new food/nutrient/disorder. A POST request will save this user request in a database, which can be reviewed by a site admin. Called by `/request_info`.


### `requirements.txt`, `writer.py` and `info.csv`
`requirements.txt` contains the modules needed to run this app.
`writer.py` contains Python code to load the nutrients and disorders into the database when running the application, from `info.csv`. See [How to Run](## How to Run) for more info.


## How the pizza toppings are generated
### Getting user preferences
At the `pizza_prefs.html` page, the user can input their dietary preferences. They can choose between veg and non-veg, and can also give the allergies they have (spice allergies, lactose intolerance, fish product allergies).
The way this happens is as follows:
 1. When the radio for "veg" is checked, a hidden input field with name "isveg" in a hidden form takes the value "true". Otherwise the field has value "false".
 2. For the allergies section, when the "None" checkbox is clicked, all other checkboxes are removed. When a checkbox for an allergy is clicked, the check ir removed from "None". This is done using JavaScript code in the file `pizza_prefs.js`.
 3. When the "Next" button is clicked, a disclaimer is shown. The user must check the radio confirming that they have read the disclaimer, and only then can they click the "Next" button again.
 4. Finally, the form is hidden and the user's choices are displayed once the button is clicked. The user can either "confirm" their choices or go back.
 5. For the allergies, multiple values can be checked, so it was necessary to send it as one list of allergies. Upon reading the disclaimer and accepting the consent form, the user's allergy choices are updated as a string. For instance, if I choose the options `Lactose-intolerance` and `Spice`, the JavaScript code will update the string as `"dairy spice"`. This is because multiple possible combinations of allergies are possible, and sending them as a list would be impractical. All this is done using JavaScript.
 6. In the hidden form, a hidden input field with name "allergies" is updated with this string value.
 7. Once the user confirms their choices, the request is sent to the backend, to the `/pizza-prefs` route for processing.

### Processing the user preferences
In the `pizza_prefs` view function, the POST request is processed and a list of foods with the required nutrient is generated and filtered for the user's dietary preferences. The way this happens is as follows:
 1. The user's preference between veg and non-veg is recorded as either `True` or `False`.
 2. The string containing the allergies is recorded
 3. The `map_allergy` function from `util.py` is used to map the allergies in the string to the values as they are recorded in the database. For example, `"dairy spice"` will be mapped to `["Dairy product", "Spice]`. This is only done if the user had input some allergies; if the string was `"none"`, then no mapping would be needed. The mapping is done due to the difference in the values used for the allergy types in the frontend and in the database.
 4. A list of foods that contain the required nutrient (say Vitamin D) is retrieved from the database.
 5. The list is filtered based on the dietary preferences. For example if the preferences are `isveg = True` and `["Dairy product", "Spice"]`, then foods that have dairy, nonveg foods, and spices are all filtered out from the list.
 6. This list of filtered foods is declared as a global variable, along with the nutrient. The function redirects the user to the `/pizza-gen` route.


### Generating the toppings list
In the `generate_pizza` view function, the global variables containing the nutrient, disorder and the list of foods (as filtered previously) are used to further process the list of possible toppings that are displayed to the user. The steps are as follows:
 1. Each food item in the list is checked for its type; based on this its weight, and subsequently its nutrient content are filtered. For instance, following the example of Vitamin D, if the food item is "Chanterelle mushrooms" (type = mushroom), then its weight is set as 120 grams. Since it contains 210 IU of vitamin D per 100 grams, its nutrient content is determined as `210/100 * 120 = 252 IU`. In case of decimals, the value is rounded to the nearest whole number.
 3. The food item, weight of topping, amount of nutrient and the unit of measurement are stored in a tuple, which is appended to a list of foods. In the example above, the tuple would be `(<Chanterelle mushrooms>, 120, 252, "IU")`.
 4. The next thing to do is to make an "optimized" pizza. This will have one topping of each food category (dressing, cheese, meat, fish, vegetable/fruit, mushroom) that contains the nutrient in the highest amount for its category. By the nature of the nutrient itself, some food groups don't have the given nutrient, so will be eliminated (ex: vitamin D is not found in any vegetable or fruit). In our case, given the user preferences of veg food without dairy or spice that contains vitamin D, the toppings will be as follows:
    - Cheese: dairy is eliminated, so lactose-free cheese is recommended instead
    - Dressing: no dressing contains the vitamin
    - Meat and fish: eliminated
    - Vegetables: no vegetables have vitamin D
    - Mushrooms: both Shitake and Chanterelle mushrooms have vitamin D, but Shitake has a greater vitamin D content (318 IU per 100 grams vs 210 IU per 100 grams), so it is chosen
 5. This optimized list of toppings can be recommended to the user, so it is kept ready for use.
 6. A list of alternative toppings is also provided to the user, so they can pick their combination of toppings to use on their pizza. This list is made from those foods which are not in the optimal toppings list but were initially filtered.
 7. The total amount of the nutrient present in the pizza is calculated. In our example, the nutrient content would be as follows:
    - Lactose-free cheddar has 75 IU of vitamin D per 100 grams, so 120 grams of it has 90 IU of vitamin D
    - Shitake mushrooms have 318 IU of vitamin D per 100 grams, so 120 grams of it has 382 IU of vitamin D
    - The total vitamin D content would then be 90 + 382 = 472 IU
 8. The percentage of the DRI(daily recommended intake) is also calculated from this value, as follows:
    - DRI of vitamin D is 1000 to 2000 IU
    - The pizza contains 472 IU
    - Based on upper and lower bounds, the % of DRI that the pizza contains would be 24 to 47 %
 9. If the % of DRI is > 110 %, then there is a chance of overdosing, so the user is given a warning and a recommendation to reduce the quantity of one or more topping.
 10. The list of optimal toppings, alternate toppings, amount of the nutrient, and % of DRI are then rendered in `pizza.html` on the `/pizza-gen` route.


## Distinctiveness and Complexity
I feel that the process detailed above is sufficiently complex to meet the requirements for the project. There was extensive testing and debugging required for these processes, as well as the other features. A total of 7 models were used, along with JavaScript for various events and data handling on the frontend. Media queries and relative styling were used to make the app mobile responsiveness, and the app was tested out on a variety of screen sizes, as below:
 - iPhone 11 Pro (375 x 812) and Pro Max (414 x 896)
 - iPhone 12/13 + Pro (390 x 844), mini (375 x 812), and Pro Max (428 x 926)
 - iPhone SE 2nd Gen (375 x 667)
 - iPhone XS (375 x 812), XS Pro and XS Max (414 x 896)
 - Google Pixel 2 (411 x 731) and 5 (393 x 851)
 - LG Optimus L70 (384 x 640)
 - Galaxy Note S10/S10+ (360 x 760), 20 (412 x 915), 20 Ultra (412 x 883), S20 (360 x 800), S20 Ultra (412 x 915), S20+ (384 x 854)
 - Kindle Fire HDX (800 x 1280)
 - iPad (810 x 1080) and iPad mini (768 x 1024)
 - 13 inch Dell screen (2160 x 1980)
 - MacBook Pro 15 inch (2880 x 1800)
 - 17 inch screen (3840 x 2160)
 - Own screen resolution (1440 x 1080)

The project is also distinct from all the other projects, including the old CS50W Pizza project. That project involved making an online menu for pizzas on which a user could place orders. My app instead gives a list of toppings that could be used to make a pizza and that have a nutrient needed to help with a particular disorder.

## How to run
First download the required `markdown` module as in `requirements.txt`. These files already contain the required database, since the nutrient, food and disease info needs to be pre-loaded, so the app can be run/hosted directly using the `runserver` argument:
```
python manage.py runserver
```