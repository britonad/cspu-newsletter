from flask_wtf import FlaskForm
from wtforms.fields import FileField, StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length


class EmailForm(FlaskForm):
    email = StringField(label='E-mail', validators=[Email()])


class ListForm(FlaskForm):
    page = StringField(validators=[Length(min=4, max=8)])
    address = StringField(validators=[Email()])
    limit = IntegerField(default=100)

    class Meta:
        csrf = False


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
