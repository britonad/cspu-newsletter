from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import Length, DataRequired


class EmailForm(FlaskForm):
    email = StringField(validators=[validators.Email()])


class MessageForm(FlaskForm):
    subject = StringField(
        label='Тема листа',
        validators=[Length(min=2, max=256)]
    )
    message = TextAreaField(
        label='Вміст',
        validators=[DataRequired()]
    )
