from flask import redirect, url_for, render_template
from flask_login import logout_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms.validators import ValidationError
from services.UserService import UserService
from services.forms import LoginForm, RegisterForm
from services.data_obtainer import Member


def login_route(db):
    user_service = UserService(db)
    form = LoginForm()

    if form.validate_on_submit():
        phone_number = form.phoneNumber.data
        input_password = form.password.data

        user_record = user_service.get_user_by_phone_number(phone_number)

        if user_record and check_password_hash(user_record.password, input_password):
            member_details = user_service.get_user_details_by_id(user_record.memberid)

            if member_details:
                member = Member(
                    member_id=member_details.member_id,
                    name=member_details.member_name,
                    surname=member_details.member_surname,
                    phone=member_details.member_phone,
                    balance=member_details.balance,
                    membership_end_date=member_details.membership_enddate,
                    membership_type=member_details.membership_type,
                    membership_id=member_details.membershipid,
                    coach_full_name=member_details.coach_full_name,
                    password=member_details.password
                )
                logout_user()
                login_user(member)
                return redirect(url_for('home'))

            form.error_message = 'Невірні дані користувача'
        else:
            form.error_message = 'Неправильний номер телефону або пароль'

    return render_template('login.html', form=form)


def register_route(db):
    user_service = UserService(db)
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            form.validate_phone_number(form.phone_number)
        except ValidationError as e:
            form.phone_number.errors.append(str(e))
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(form.password.data, method='scrypt')
        user_service.insert_user(form, hashed_password)

        return redirect(url_for('login'))

    return render_template('register.html', form=form)
