from flask_ckeditor import CKEditorField
from flask_ckeditor.fields import CKEditor
from flask_wtf import FlaskForm
from sqlalchemy.testing.pickleable import Mixin
from wtforms import StringField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import SubmitField, TextAreaField, PasswordField, URLField
from wtforms.validators import DataRequired, Optional


class MyForm(FlaskForm):
    title = StringField('Give title', validators=[DataRequired()])

    subtitle = StringField('Give Subtitle', validators=[DataRequired()])

    date = DateField('give date', validators=[DataRequired()])

    image_uri = StringField('Give image URI', validators=[DataRequired()])

    body = TextAreaField('Give context of post', validators=[DataRequired()])
    submit = SubmitField("submit")



class EditPostForm(FlaskForm):
    title = StringField("Title (optional)", validators=[Optional()])
    subtitle = StringField("Subtitle (optional)", validators=[Optional()])
    img_url = URLField("Image URL (optional)", validators=[Optional()])
    body = TextAreaField("Body (optional)", validators=[Optional()])
    submit = SubmitField("Save Changes")

class register_form(FlaskForm,Mixin):
    name = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    register = SubmitField("Register")

class login_form(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Log In")

class CommentForm(FlaskForm):
    body = CKEditorField("Give your comment text", validators=[DataRequired()])
    submit = SubmitField("Submit")