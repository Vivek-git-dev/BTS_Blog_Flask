from app.extensions import db
from slugify import slugify


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(self.name)


# Many-to-Many Relationship Table
class PostCategory(db.Model):
    __tablename__ = "post_categories"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    def __repr__(self):
        return f"<PostCategory post={self.post_id}, category={self.category_id}>"
