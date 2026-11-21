"""
scripts/refine_index_html.py
Clean up raw emoji clutter and refine hero typography in frontend/index.html
Grounded in Anthropic Frontend Design skill principles.
"""

import re

INDEX_PATH = "frontend/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Category strip replacements
replacements = [
    ("🏠 Student PGs", "Student PGs"),
    ("🏢 Rental Flats", "Rental Flats"),
    ("💻 Laptops & PCs", "Laptops & Computers"),
    ("📱 Mobiles", "Mobiles & Tablets"),
    ("🏍️ Bikes & Scooters", "Bikes & Scooters"),
    ("🛋️ Study Desks & Beds", "Study Desks & Beds"),
    ("📚 Gate & Tech Books", "GATE & Tech Books"),
    ("❄️ Coolers & Appliances", "Coolers & Appliances"),
    ("⚡ Verified Deals", "Verified Deals"),
    ("🎓 Near Graphic Era (GEU)", "Graphic Era (GEU / GEHU)"),
    ("🎓 Near UPES (Bidholi/Kandoli)", "UPES (Bidholi / Kandoli)"),
    ("🎓 Near DIT University", "DIT University"),
    ("💻 Laptops under ₹35,000", "Laptops under ₹35,000"),
    ("🏠 PGs under ₹7,000 (With Food)", "PGs under ₹7,000 (With Food)"),
    ("🏍️ Scooters & Activas", "Scooters & Activas"),
    ("📢 Moving out or got extra gear?", "List a Room or Sell Campus Gear"),
    ("📂 Explore Popular Categories", "Explore Popular Categories"),
    ("🏠 Student Accommodations in Dehradun", "Student Accommodations in Dehradun"),
    ("🛒 Fresh Student Classifieds (Buy & Sell)", "Fresh Student Classifieds (Buy & Sell)"),
    ("🔥 Trending PG & Rental Listings", "Trending PG & Rental Listings"),
    ("💡 Student Savings Calculator", "Student Savings Calculator"),
    ("📊 Dehradun Student Market Trends", "Dehradun Student Market Trends"),
    ("🏠 Housing & Brokerage", "Housing & Brokerage"),
    ("🎒 Campus Gear Re-Commerce", "Campus Gear Re-Commerce"),
    ("🏠 Student Accommodation Rent by Campus Zone", "Accommodation Rent by Campus Zone"),
    ("🛒 Student Re-Commerce Pricing & Savings", "Student Re-Commerce Pricing & Savings"),
    ("Uttarakhand's Student & Rental <span class=\"highlight\">Marketplace</span>", "Student Accommodation & Classifieds Across Uttarakhand"),
]

for old, new in replacements:
    html = html.replace(old, new)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Updated frontend/index.html cleanly!")

