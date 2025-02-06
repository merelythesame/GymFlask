from flask import redirect, url_for, render_template
from flask_login import logout_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms.validators import ValidationError

from services.forms import LoginForm, RegisterForm
from sqlalchemy.sql import text

from services.data_obtainer import Member


def login_route(db):
    print()
    form = LoginForm()
    if form.validate_on_submit():
        phone_number = form.phoneNumber.data
        input_password = form.password.data

        user_record = db.session.execute(
            text("SELECT * FROM Members WHERE phoneNumber = :phoneNumber;"),
            {'phoneNumber': phone_number}
        ).fetchone()

        if user_record:
            stored_password_hash = user_record.password
            member_id = user_record.memberid
            print(member_id)

            if check_password_hash(stored_password_hash, input_password):
                member_details = db.session.execute(
                    text("SELECT * FROM getmemberdetailsbyid(:member_id);"),
                    {'member_id': member_id}
                ).fetchone()

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
            else:
                form.error_message = 'Неправельний пароль'
        else:
            form.error_message = 'Неправельний номер телефону'

    return render_template('login.html', form=form)


def register_route(db):
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            form.validate_phone_number(form.phone_number)
        except ValidationError as e:
            form.phone_number.errors.append(str(e))
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(form.password.data, method='scrypt')
        db.session.execute(
            text("""CALL InsertUser(:name,:surname,:phone,:password,:membershipId,:balance)"""),
            {
                'name': form.name.data,
                'surname': form.last_name.data,
                'phone': form.phone_number.data,
                'password': hashed_password,
                'membershipId': None,
                'balance': 0.00
            }
        )
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)