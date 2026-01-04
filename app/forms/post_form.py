from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, IntegerField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length, URL, Optional

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    slug = StringField("Slug (URL)", validators=[DataRequired(), Length(max=250)])

    summary = TextAreaField("Summary", validators=[Optional(), Length(max=300)])

    content = TextAreaField("Content", validators=[DataRequired()])

    image_url = StringField("Image URL", validators=[Optional(), URL(), Length(max=300)])

    categories = SelectMultipleField("Categories", coerce=int)

    is_published = BooleanField("Publish?")
    read_time = IntegerField("Read Time (minutes)", default=1)

    submit = SubmitField("Create Post")
