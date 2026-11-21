"""
scripts/refine_search_pages.py
Refine search-properties.html and search-products.html to eliminate
cheap/generic emoji clutter and apply clean, professional text labels.
"""

def refine_properties():
    path = "frontend/search-properties.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    replacements = [
        ("🏠 Student PGs (Food Inc.)", "Student PGs (Meals Included)"),
        ("🏢 Hostels", "Campus Hostels"),
        ("🛋️ Independent Flats", "Independent Flats"),
        ("🛏️ Single Private Rooms", "Single Private Rooms"),
        ("👨 Boys Only", "Boys Accommodations"),
        ("👩 Girls Only", "Girls Accommodations"),
        ("🛒 Student Re-Commerce", "Student Re-Commerce"),
        ("🏠 Accommodations", "Accommodations"),
        ("🛒 Buy & Sell", "Buy & Sell"),
        ("WiFi 📶", "High-Speed WiFi"),
        ("Meals 🍲", "Homestyle Meals"),
        ("Hot Water 🚿", "Geyser / Hot Water"),
        ("Security 🛡️", "24/7 Security & CCTV"),
        ("Cleaning 🧹", "Daily Housekeeping"),
        ("Laundry 🧺", "Laundry Machine"),
        ("Parking 🅿️", "Two-Wheeler Parking"),
        ("Cities We Serve 🏔️", "Uttarakhand Hubs"),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Refined search-properties.html")

def refine_products():
    path = "frontend/search-products.html"
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
        ("Cities We Serve 🏔️", "Uttarakhand Hubs"),
    ]
    for old, new in replacements:
        html = html.replace(old, new)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Refined search-products.html")

if __name__ == "__main__":
    refine_properties()
    refine_products()

