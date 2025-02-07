from math import ceil
from flask import redirect, url_for, render_template, flash, request
from flask_login import current_user, logout_user
from services.UserService import UserService
from services.forms import DepositForm, EditPasswordForm, MembershipForm, PaymentsForm
from services.data_obtainer import get_all_coaches_to_pick, get_all_available_memberships, get_all_coaches


def home_route(db):
    user_service = UserService(db)
    deposit_from = DepositForm()
    password_form = EditPasswordForm()

    if deposit_from.validate_on_submit():
        user_service.process_deposit(deposit_from.amount.data, deposit_from.payment_type.data, current_user.member_id)
        flash('Поповнення успішне!', 'success')
        return redirect(url_for('home'))

    if password_form.validate_on_submit():
        if not user_service.change_password(current_user.member_id, password_form.old_password.data, password_form.new_password.data, current_user.password):
            flash('Неправильний старий пароль', 'danger')
            return redirect(url_for('home'))

        flash('Ваш пароль успішно змінено', 'success')
        return redirect(url_for('home'))

    return render_template('home.html', current_user=current_user, deposit_from=deposit_from, password_form=password_form)


def memberships_route(db):
    user_service = UserService(db)
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
                user_service.assign_membership_to_member(membership_id, current_user.member_id, form.picked_coach.data)
                flash('Абонемент успішно отриманий!', 'success')
                return redirect(url_for('memberships'))

    return render_template('memberships.html', memberships=memberships, form=form, membership_id=str(current_user.membership_id))


def coaches_route(db):
    coaches = get_all_coaches(db)
    return render_template('coaches.html', coaches=coaches)


def payments_route(db):
    user_service = UserService(db)
    form = PaymentsForm()
    sort_column = 'dateofpayment'
    sort_order = 'DESC'

    if form.validate_on_submit():
        sort_option = form.sort_type.data
        sort_column, sort_order = sort_option.split('_')

    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page

    total_payments = user_service.execute_db_query(
        "SELECT COUNT(*) FROM Payments WHERE memberId = :member_id",
        {'member_id': current_user.member_id}, fetch_one=True)[0]

    total_pages = ceil(total_payments / per_page)

    payments = user_service.execute_db_query(
        "SELECT * FROM GetSortedPayments(:member_id, :sort_column, :sort_order) LIMIT :limit OFFSET :offset",
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