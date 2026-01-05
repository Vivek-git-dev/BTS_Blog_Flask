from app import create_app
from app.models.category import Category
from app.extensions import db

app = create_app()

with app.app_context():
    categories = [
        # Existing categories
        Category(name="Technology"),
        Category(name="Lifestyle"),
        Category(name="Business"),
        Category(name="Health"),
        Category(name="Travel"),

        # Development & tech journey
        Category(name="Web Development Journey"),
        Category(name="Backend & APIs"),
        Category(name="Deployment & Hosting"),
        Category(name="Tech Stack & Tools"),
        Category(name="Learning & Productivity"),
        Category(name="Project Diaries"),

        # Personal interests
        Category(name="Movies & Documentaries"),
        Category(name="Insurance & Personal Finance"),
        Category(name="Fitness & Outdoor Sports"),
        Category(name="Thoughts & Reflections"),

        # Book-related categories
        Category(name="Book Reflections"),
        Category(name="Recommended Reads"),
        Category(name="Ideas from Books"),
    ]

    for cat in categories:
        cat.generate_slug()
        # Check if category already exists
        existing = Category.query.filter_by(name=cat.name).first()
        if not existing:
            db.session.add(cat)
    
    db.session.commit()
    print("Categories added successfully!")
