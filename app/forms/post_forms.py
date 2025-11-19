from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, BooleanField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length, URL
from flask_ckeditor import CKEditorField
from app.models.category import Category


class PostForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(min=3, max=200)]
    )

    summary = StringField(
        "Summary",
        validators=[Length(max=300)]
    )

    content = CKEditorField(
        "Content",
        validators=[DataRequired()]
    )

    image_url = URLField(
        "Featured Image URL",
        validators=[URL(), Length(max=300)],
        description="Paste an image URL from Unsplash, Cloudinary, or your DB"
    )

    categories = SelectMultipleField(
        "Categories",
        coerce=int
    )

    is_published = BooleanField("Publish now?")

    submit = SubmitField("Save Post")

    # Load categories dynamically each time form is created
    def set_category_choices(self):
        self.categories.choices = [(c.id, c.name) for c in Category.query.all()]
