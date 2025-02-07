from sqlalchemy.sql import text
from flask import render_template, redirect, url_for
from services.AdminService import AdminService
from services.forms import AddMembershipForm
from services.data_obtainer import get_all_available_memberships


def manage_memberships_route(db, app):
    admin_service = AdminService(db, app)
    session = admin_service.get_db_session()
    memberships = get_all_available_memberships(db)
    form = AddMembershipForm()

    if form.validate_on_submit():
        params = {
            'type': form.type.data,
            'price': form.price.data,
            'description': form.description.data,
            'hascoach': form.hascoach.data
        }
        admin_service.execute_db_query(session, """CALL InsertAvailableMembership(:type, :price, :description, :hascoach)""", params)
        session.close()
        return redirect(url_for('.manage_memberships'))

    return render_template('manage_membership.html', form=form, memberships=memberships)


def edit_membership_route(membership_id, db, app):
    admin_service = AdminService(db, app)
    session = admin_service.get_db_session()
    membership_raw = session.execute(text("""SELECT * FROM AvailableMemberships WHERE membershipId = :membership_id"""),
                                    {'membership_id': membership_id}).fetchone()

    if not membership_raw:
        session.close()
        return redirect(url_for('.manage_memberships'))

    membership = {
        'membershipid': str(membership_raw.membershipid),
        'type': membership_raw.type,
        'price': float(membership_raw.price),
        'description': membership_raw.description,
        'hascoach': bool(membership_raw.hascoach)
    }

    form = AddMembershipForm()

    if form.validate_on_submit():
        params = {
            'membership_id': membership_id,
            'type': form.type.data,
            'price': form.price.data,
            'description': form.description.data,
            'hascoach': form.hascoach.data
        }
        admin_service.execute_db_query(session, """CALL UpdateAvailableMembership(:membership_id, :type, :price, :description, :hascoach)""", params)
        session.close()
        return redirect(url_for('.manage_memberships'))

    session.close()
    return render_template('edit_membership.html', form=form, membership=membership)


def delete_membership_route(membership_id, db, app):
    admin_service = AdminService(db, app)
    session = admin_service.get_db_session()
    admin_service.execute_db_query(session, """CALL DeleteAvailableMembership(:membership_id)""", {'membership_id': membership_id})
    session.close()
    return redirect(url_for('.manage_memberships'))