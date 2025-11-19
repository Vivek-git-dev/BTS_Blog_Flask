from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.post import Post
from app.models.category import Category
from app.models.comment import Comment
from markupsafe import Markup
from slugify import slugify

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # --------------------
    # Users
    # --------------------
    user1 = User(name="Vivek", email="vivek@example.com", password="test123", role="admin")
    user2 = User(name="John Doe", email="john@example.com", password="test123", role="reader")

    db.session.add_all([user1, user2])
    db.session.commit()

    # --------------------
    # Categories
    # --------------------
    tech = Category(name="Tech", slug="tech")
    python = Category(name="Python", slug="python")
    life = Category(name="Lifestyle", slug="lifestyle")

    db.session.add_all([tech, python, life])
    db.session.commit()

    # --------------------
    # Posts
    # --------------------
    post1 = Post(
        title="Getting Started With Flask",
        slug=slugify("Getting Started With Flask"),
        summary="A simple guide to understanding the basics of Flask.",
        content=Markup("<p>Welcome to Flask! This is a simple introduction...</p>"),
        image_url="https://images.unsplash.com/photo-1522199710521-72d69614c702",
        author_id=user1.id,
        is_published=True
    )
    post1.categories.extend([tech, python])

    post2 = Post(
        title="Why Python is Awesome",
        slug=slugify("Why Python is Awesome"),
        summary="Python is one of the most versatile languages. Here's why.",
        content=Markup("<p>Python is powerful, easy to read, and great for beginners...</p>"),
        image_url="https://images.unsplash.com/photo-1584697964191-33512e6b89c0",
        author_id=user1.id,
        is_published=True
    )
    post2.categories.append(python)

    db.session.add_all([post1, post2])
    db.session.commit()

    # --------------------
    # Comments
    # --------------------
    comment1 = Comment(
        content="Great article, thanks!",
        post_id=post1.id,
        author_name="Random User"
    )

    comment2 = Comment(
        content="Very helpful explanation.",
        post_id=post2.id,
        user_id=user2.id
    )

    db.session.add_all([comment1, comment2])
    db.session.commit()

    print("Sample data inserted successfully!")
