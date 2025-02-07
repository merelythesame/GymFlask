from math import ceil
from flask import redirect, url_for, render_template, flash, request
from flask_login import current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from services.forms import DepositForm, EditPasswordForm, MembershipForm, PaymentsForm
from sqlalchemy.sql import text
from services.data_obtainer import get_all_coaches_to_pick, get_all_available_memberships, get_all_coaches


def execute_db_query(session, query, params=None, fetch_one=False, fetch_all=False, commit=False):
    result = session.execute(text(query), params or {})

    if fetch_one:
        return result.fetchone()
    if fetch_all:
        return result.fetchall()
    if commit:
        session.commit()


def process_deposit(db, amount, payment_type):
    execute_db_query(db.session,"CALL deposit(:id, :amount, :type)",
{'id': current_user.member_id, 'amount': amount, 'type': payment_type}, commit=True)


def change_password(db, old_password, new_password):
    if not check_password_hash(current_user.password, old_password):
        return False

    hashed_password = generate_password_hash(new_password, method='scrypt')

    execute_db_query(db.session,"CALL EditUserPassword(:userId, :newPassword)",
{'userId': current_user.member_id, 'newPassword': hashed_password}, commit=True)
    return True


def assign_membership_to_member(db, membership_id, coach_id=None):
    query = "CALL AssignMembershipToMember(:userId, :membership_id" + (", :coach_id" if coach_id else "") + ")"
    params = {'userId': current_user.member_id, 'membership_id': membership_id}

    if coach_id:
        params['coach_id'] = coach_id

    execute_db_query(db.session, query, params, commit=True)


def home_route(db):
    deposit_from = DepositForm()
    password_form = EditPasswordForm()

    if deposit_from.validate_on_submit():
        process_deposit(db, deposit_from.amount.data, deposit_from.payment_type.data)
        flash('Поповнення успішне!', 'success')
        return redirect(url_for('home'))

    if password_form.validate_on_submit():
        if not change_password(db, password_form.old_password.data, password_form.new_password.data):
            flash('Неправильний старий пароль', 'danger')
            return redirect(url_for('home'))

        flash('Ваш пароль успішно змінено', 'success')
        return redirect(url_for('home'))

    return render_template('home.html', current_user=current_user, deposit_from=deposit_from, password_form=password_form)


def memberships_route(db):
    memberships = get_all_available_memberships(db)
    form = MembershipForm()
    form.picked_coach.choices = get_all_coaches_to_pick(db)

    if request.method == 'POST':
        membership_id = request.form.get('membership_id')
        membership_ids = set([membership['membershipid'] for membership in memberships])

        if membership_id in membership_ids:
            membership = next(membership for membership in memberships if membership['membershipid'] == membership_id)

            if membership['price'] > current_user.balance:
                flash('Недостатньо коштів на рахунку', 'danger')
            else:
                assign_membership_to_member(db, membership_id, form.picked_coach.data)
                flash('Абонемент успішно отриманий!', 'success')
                return redirect(url_for('memberships'))

    return render_template('memberships.html', memberships=memberships, form=form, membership_id=str(current_user.membership_id))


def coaches_route(db):
    coaches = get_all_coaches(db)
    return render_template('coaches.html', coaches=coaches)


def payments_route(db):
    form = PaymentsForm()
    sort_column = 'dateofpayment'
    sort_order = 'DESC'

    if form.validate_on_submit():
        sort_option = form.sort_type.data
        sort_column, sort_order = sort_option.split('_')

    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    total_payments = execute_db_query(db.session,"SELECT COUNT(*) FROM Payments WHERE memberId = :member_id",
        {'member_id': current_user.member_id}, fetch_one=True)[0]

    total_pages = ceil(total_payments / per_page)

    payments = execute_db_query(db.session,"SELECT * FROM GetSortedPayments(:member_id, :sort_column, :sort_order)LIMIT :limit OFFSET :offset",
        {
            'member_id': current_user.member_id,
            'sort_column': sort_column,
            'sort_order': sort_order,
            'limit': per_page,
            'offset': offset
        }, fetch_all=True)

    return render_template('payments.html', form=form, payments=payments, current_page=page, total_pages=total_pages)


def logout_route():
    logout_user()
    return redirect(url_for('login'))