from django.core.files.storage import default_storage

# gets detailed entry about nutrient/disorder (if available)
def get_entry(type, title):
    try:
        f = default_storage.open(f"detailed_entries/{type}/{title.lower()}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


# maps the allergies to standard names via the mapping code
def map_allergies(allergies, mapping={
    "fish": "Fish product",
    "dairy": "Dairy product",
    "spice": "Spice"
}):
    x = []
    for allergy in allergies:
        a = mapping.get(allergy, None)
        if a:
            x.append(a)

    if x == []:
        return "none"
    
    return x