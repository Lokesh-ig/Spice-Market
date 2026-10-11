from django.core.management.base import BaseCommand
from api.models import Product

class Command(BaseCommand):
    help = 'Seeds initial spice products for the Spice Market website'

    def handle(self, *args, **kwargs):
        initial_products = [
            {
                "name": "Turmeric Powder",
                "price": 180.00,
                "image_url": "img_1.png.png",
                "category": "Organic Spices",
                "description": "Pure organic golden turmeric ground to perfection with high curcumin content.",
                "stock": 150
            },
            {
                "name": "Red Chilli Powder",
                "price": 240.00,
                "image_url": "img_2.png.png",
                "category": "Organic Spices",
                "description": "Vibrant red spicy chilli powder bringing rich color and authentic heat to every dish.",
                "stock": 120
            },
            {
                "name": "Clove Powder",
                "price": 480.00,
                "image_url": "img_3.png.png",
                "category": "Aromatic Spices",
                "description": "Premium aromatic ground clove harvested from tropical farms, providing deep warming essence.",
                "stock": 80
            },
            {
                "name": "Gram Masala",
                "price": 220.00,
                "image_url": "img_4.png.png",
                "category": "Spice Blends",
                "description": "Traditional roasted masala blend crafted with heritage family recipes for rich curries.",
                "stock": 200
            },
            {
                "name": "Pepper Powder",
                "price": 280.00,
                "image_url": "img_5.png.png",
                "category": "Organic Spices",
                "description": "Freshly cracked black peppercorns offering robust pungency and crisp warmth.",
                "stock": 140
            },
            {
                "name": "Cinnamon Powder",
                "price": 320.00,
                "image_url": "img_6.png.png",
                "category": "Aromatic Spices",
                "description": "Sweet, fragrant Ceylon cinnamon finely ground for curries, bakes, and teas.",
                "stock": 95
            },
            {
                "name": "Coriander Powder",
                "price": 190.00,
                "image_url": "img_7.png.png",
                "category": "Organic Spices",
                "description": "Sun-dried organic coriander seeds gently stone-ground for citrusy and nutty flavor notes.",
                "stock": 110
            },
            {
                "name": "Milk Powder",
                "price": 420.00,
                "image_url": "img_8.png.png",
                "category": "Dairy Essentials",
                "description": "Rich full-cream milk powder ideal for traditional Indian sweets and hot beverages.",
                "stock": 60
            },
            {
                "name": "Cumin Powder",
                "price": 210.00,
                "image_url": "img_9.png.png",
                "category": "Organic Spices",
                "description": "Lightly roasted cumin seeds with warm earthy fragrance, an everyday pantry essential.",
                "stock": 180
            },
            {
                "name": "Cardamom Powder",
                "price": 520.00,
                "image_url": "img_10.png",
                "category": "Aromatic Spices",
                "description": "Exquisite hand-picked green cardamom pods stone-ground for rich sweet-spicy aroma.",
                "stock": 75
            },
            {
                "name": "Kashmiri Saffron",
                "price": 850.00,
                "image_url": "img_11.png",
                "category": "Royal Spices",
                "description": "Pure grade-A Kashmiri Mongra saffron threads offering royal aroma and vivid golden hue.",
                "stock": 40
            },
            {
                "name": "Star Anise",
                "price": 310.00,
                "image_url": "img_12.png",
                "category": "Aromatic Spices",
                "description": "Sun-dried whole star anise pods with fragrant liquorice warmth for biryanis and stews.",
                "stock": 90
            },
            {
                "name": "Mustard Seeds",
                "price": 160.00,
                "image_url": "img_13.png",
                "category": "Organic Spices",
                "description": "Organic black mustard seeds with zesty pungent crackle for traditional Indian tadka.",
                "stock": 160
            },
            {
                "name": "Fenugreek Seeds",
                "price": 170.00,
                "image_url": "img_14.png",
                "category": "Organic Spices",
                "description": "Aromatic golden fenugreek seeds delivering distinctive savory maple-bitter culinary depth.",
                "stock": 130
            },
            {
                "name": "Nutmeg & Mace",
                "price": 440.00,
                "image_url": "img_15.png",
                "category": "Aromatic Spices",
                "description": "Fragrant tropical nutmeg and delicate scarlet mace bladed for royal festive gravies.",
                "stock": 65
            }
        ]

        created_count = 0
        updated_count = 0
        for item in initial_products:
            obj, created = Product.objects.update_or_create(
                name=item["name"],
                defaults={
                    "price": item["price"],
                    "image_url": item["image_url"],
                    "category": item["category"],
                    "description": item["description"],
                    "stock": item["stock"],
                    "is_active": True
                }
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {created_count} new products and updated {updated_count} products."))
