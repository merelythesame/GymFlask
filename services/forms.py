from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, ValidationError, DecimalField, BooleanField, FileField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp
import re
from wtforms.validators import DataRequired, Optional

class LoginForm(FlaskForm):
    phoneNumber = StringField('Номер телефону', validators=[InputRequired(), Length(min=10, max=15)])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=4, max=150)])
    submit = SubmitField('Вхід')
    error_message = None


class DepositForm(FlaskForm):
    payment_type = SelectField('Тип оплати', choices=[
        ('Paypal', 'Paypal'),
        ('Payoneer', 'Payoneer'),
        ('Card', 'Card')
    ], validators=[InputRequired()])

    amount = StringField('Сума', validators=[InputRequired(), Length(min=1, max=10)])
    submit = SubmitField('Поповнити')

class EditPasswordForm(FlaskForm):
    old_password = PasswordField('Старий пароль', validators=[InputRequired()])
    new_password = PasswordField('Новий пароль', validators=[InputRequired(), Length(min=6)])
    confirm_password = PasswordField('Підтвердіть новий пароль', validators=[
        InputRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Змінити пароль')

class MembershipForm(FlaskForm):
    picked_coach = SelectField('Виберіть тренера', choices=[], validators=[InputRequired()])
    submit = SubmitField('Отримати')

class PaymentsForm(FlaskForm):
    sort_type = SelectField(
        'Сортування:',
        choices=[
            ('dateofpayment_DESC', 'За датою від новіших'),
            ('dateofpayment_ASC', 'За датою від старіших'),
            ('price_ASC', 'За ціною від меншої'),
            ('price_DESC', 'За ціною від більшої'),
            ('typeofservice_DESC', 'За призначенням')
        ],
        validators=[InputRequired()]
    )

class RegisterForm(FlaskForm):
    name = StringField('Ім\'я', validators=[InputRequired(), Length(min=2, max=255)])
    last_name = StringField('Прізвище', validators=[InputRequired(), Length(min=2, max=255)])
    phone_number = StringField('Номер телефону', validators=[InputRequired(), Length(min=10, max=15)])
    password = PasswordField('Пароль', validators=[InputRequired(), Length(min=6, max=255)])
    confirm_password = PasswordField('Підтвердіть пароль', validators=[
        InputRequired(),
        EqualTo('password', message='Паролі не збігаються')
    ])
    submit = SubmitField('Register')
    error_message = None

    def validate_phone_number(self, field):
        phone_pattern = r'^(\+380|0)?\d{9,12}$'
        if not re.match(phone_pattern, field.data):
            raise ValidationError('Некоректний формат номеру телефону.')


class AddMembershipForm(FlaskForm):
    type = StringField('Тип абонементу', validators=[DataRequired()])
    price = DecimalField('Ціна', places=2, validators=[DataRequired()])
    description = StringField('Опис', validators=[Optional()])
    hascoach = BooleanField('З тренером?', default=False)

class CoachForm(FlaskForm):
    name = StringField('Ім\'я', validators=[DataRequired(), Length(max=255)])
    lastName = StringField('Прізвище', validators=[DataRequired(), Length(max=255)])
    speciality = StringField('Напрямок', validators=[DataRequired(), Length(max=255)])
    phoneNumber = StringField('Номер телефону', validators=[DataRequired(), Length(min=10, max=15)])
    photo = FileField('Завантажити фото')
    submit = SubmitField('Додати')

    def validate_phoneNumber(self, field):
        phone_pattern = r'^(\+380|0)?\d{9,12}$'
        if not re.match(phone_pattern, field.data):
            raise ValidationError('Некоректний формат номеру телефону.')
