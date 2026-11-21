"""
scripts/refine_detail_pages.py
Refine property-detail.html and product-detail.html category strips and nav links
"""

def refine_prop_detail():
    path = "frontend/property-detail.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    replacements = [
        ("🏠 Student PGs", "Student PGs"),
        ("🏢 Rental Flats", "Rental Flats"),
        ("🛏️ Hostels", "Hostels"),
        ("👨 Boys Only", "Boys Accommodations"),
        ("👩 Girls Only", "Girls Accommodations"),
        ("🛒 Student Re-Commerce", "Student Re-Commerce"),
        ("🏠 Accommodations", "Accommodations"),
        ("🛒 Buy & Sell", "Buy & Sell"),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Refined property-detail.html")

def refine_prod_detail():
    path = "frontend/product-detail.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    replacements = [
        ("💻 Laptops & PCs", "Laptops & Computers"),
        ("📱 Mobiles", "Mobiles & Gadgets"),
        ("🏍️ Bikes & Scooters", "Bikes & Scooters"),
        ("🛋️ Furniture & Desks", "Furniture & Study Desks"),
        ("📚 Academic Books", "Academic & Exam Books"),
        ("🏠 PGs & Flats", "PGs & Flats"),
        ("🏠 Accommodations", "Accommodations"),
        ("🛒 Buy & Sell", "Buy & Sell"),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Refined product-detail.html")

if __name__ == "__main__":
    refine_prop_detail()
    refine_prod_detail()

