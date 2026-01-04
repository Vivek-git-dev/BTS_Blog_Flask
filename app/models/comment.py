# app/models/comment.py
from datetime import datetime
from app import db

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    # Auto timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationship backrefs
    post = db.relationship("Post", back_populates="comments")

    def __repr__(self):
        return f"<Comment {self.id} by User {self.user_id}>"
