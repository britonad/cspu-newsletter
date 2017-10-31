from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.validators import Length, DataRequired
from wtforms.fields import StringField, TextAreaField, FileField


class EmailForm(FlaskForm):
    email = StringField(label='E-mail', validators=[validators.Email()])


class MessageForm(FlaskForm):
    subject = StringField(
        label='Тема листа',
        validators=[Length(min=2, max=256)]
    )
    message = TextAreaField(
        label='Вміст',
        validators=[DataRequired()]
    )
    file1 = FileField(label='Файл 1')
    file2 = FileField(label='Файл 2')
    file3 = FileField(label='Файл 3')
    file4 = FileField(label='Файл 4')
    file5 = FileField(label='Файл 5')
