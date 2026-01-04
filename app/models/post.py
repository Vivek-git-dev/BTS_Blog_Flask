from app.extensions import db
from datetime import datetime
from sqlalchemy.orm import relationship
from slugify import slugify   # pip install python-slugify


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False)

    summary = db.Column(db.String(300))
    content = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.String(300))

    # Foreign Key - User
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    is_published = db.Column(db.Boolean, default=False)
    read_time = db.Column(db.Integer, default=1)   # minutes
    views = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    comments = db.relationship("Comment", back_populates="post", lazy=True)

    categories = db.relationship(
        "Category",
        secondary="post_categories",     # table name created later
        backref="posts",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Post {self.title}>"

    # Generate slug automatically
    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(self.title)

    # Calculate read time
    def calculate_read_time(self):
        word_count = len(self.content.split())
        self.read_time = max(1, word_count // 200)   # avg reading speed: 200 WPM
