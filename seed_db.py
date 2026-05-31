import os
import django

# 1. Initialize the Django settings context
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import Product, Category

def seed_database():
    print("Cleaning database categories and products...")
    Product.objects.all().delete()
    Category.objects.all().delete()

    print("Creating premium clothing categories...")
    ethnic_wear = Category.objects.create(name="Ethnic Wear")
    streetwear = Category.objects.create(name="Modern Streetwear")
    essentials = Category.objects.create(name="Premium Essentials")

    products_data = [
        # Ethnic Wear Category
        {
            "category": ethnic_wear,
            "title": "Handwoven Banarasi Silk Saree",
            "description": "An exquisite heritage Banarasi silk saree handwoven by master craftsmen in Varanasi. Features ornate gold and silver zari buttis, an opulent floral border, and a rich brocade pallu. Perfect for premium celebrations and heritage curation.",
            "price": 8499.00,
            "stock": 12,
            "image": "products/2026/05/24/saree.png",
            "available": True
        },
        {
            "category": ethnic_wear,
            "title": "Lucknowi Chikankari Georgette Kurta",
            "description": "A premium Lucknowi Chikankari kurta handcrafted on ultra-soft georgette fabric. Adorned with intricate shadow work, bakhiya, and phanda embroidery patterns. Exudes timeless elegance and bespoke ethnic craftsmanship.",
            "price": 3299.00,
            "stock": 25,
            "image": "products/2026/05/24/kurta.png",
            "available": True
        },
        # Modern Streetwear Category
        {
            "category": streetwear,
            "title": "Obsidian Heavyweight Graphic Hoodie",
            "description": "An avant-garde oversized streetwear hoodie crafted from ultra-dense 400 GSM French terry cotton. Features distressed cybernetic screen-prints, drop-shoulder geometry, double-lined seamless hood, and ribbed details. Designed for modern urban supremacy.",
            "price": 2499.00,
            "stock": 30,
            "image": "products/2026/05/24/hoodie.png",
            "available": True
        },
        {
            "category": streetwear,
            "title": "Cyberpunk Techwear Cargo Trousers",
            "description": "Water-resistant tactical cargo trousers designed for active mobility. Features lightweight double-weave ripstop shell, modular utility zip pockets, adjustable nylon straps, and tapered elastic cuffs. Perfect blend of utility and streetwear visual aesthetics.",
            "price": 3899.00,
            "stock": 18,
            "image": "products/2026/05/24/cargos.png",
            "available": True
        },
        # Premium Essentials Category
        {
            "category": essentials,
            "title": "Supima Luxury Cotton Tees (Pack of 3)",
            "description": "A curated pack of three premium monochrome heavyweight tees crafted from 100% organic extra-long staple Supima cotton. Offers twice the strength and exceptional softness of standard organic cotton. Designed with a structured, relaxed-fit drape that holds shape.",
            "price": 1899.00,
            "stock": 50,
            "image": "products/2026/05/24/supima_tees.png",
            "available": True
        },
        {
            "category": essentials,
            "title": "Structured Contemporary Casual Blazer",
            "description": "A modern unstructured casual blazer engineered from a premium breathable wool-blend. Features a sharp tailored silhouette, contemporary notch lapels, sleek patch pockets, and finished with anodized matte metallic utility button accents.",
            "price": 5499.00,
            "stock": 15,
            "image": "products/2026/05/24/blazer.png",
            "available": True
        }
    ]

    print("Seeding premium boutique apparel with real photography paths...")
    for item in products_data:
        Product.objects.create(
            category=item["category"],
            title=item["title"],
            description=item["description"],
            price=item["price"],
            stock=item["stock"],
            image=item["image"],
            available=item["available"]
        )

    print("Database successfully seeded in Indian Rupees (INR) with real photo assets!")
    print(f"Added Categories: {Category.objects.count()}")
    print(f"Added Products: {Product.objects.count()}")

if __name__ == "__main__":
    seed_database()
