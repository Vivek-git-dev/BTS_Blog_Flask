from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    content = TextAreaField(
        "Write your comment",
        validators=[DataRequired(), Length(min=2, max=1000)],
        render_kw={"required": False}
    )
    submit = SubmitField("Post Comment")
