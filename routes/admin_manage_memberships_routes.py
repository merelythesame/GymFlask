from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from flask import render_template, redirect, url_for
from services.forms import AddMembershipForm
from services.data_obtainer import get_all_available_memberships


def manage_memberships_route(db, app):
    admin_engine = db.get_engine(app, bind='admin')
    Session = sessionmaker(bind=admin_engine)
    session = Session()

    memberships = get_all_available_memberships(db)

    print(memberships)
    form = AddMembershipForm()
    if form.validate_on_submit():
        membership_type = form.type.data
        price = form.price.data
        description = form.description.data
        hascoach = form.hascoach.data


        session.execute(text("""
                    Call InsertAvailableMembership(:type, :price, :description, :hascoach)
                """), {
                'type': membership_type,
                'price': price,
                'description': description,
                'hascoach': hascoach
            })
        session.commit()

        session.close()
        return redirect(url_for('.manage_memberships'))
    return render_template('manage_membership.html', form=form, memberships=memberships)

def edit_membership_route(membership_id, db, app):
    admin_engine = db.get_engine(app, bind='admin')
    Session = sessionmaker(bind=admin_engine)
    session = Session()

    membership_raw = session.execute(text("""
        SELECT * FROM AvailableMemberships WHERE membershipId = :membership_id
    """), {'membership_id': membership_id}).fetchone()

    membership = {
        'membershipid': str(membership_raw.membershipid),
        'type': membership_raw.type,
        'price': float(membership_raw.price),
        'description': membership_raw.description,
        'hascoach': bool(membership_raw.hascoach)
    }

    form = AddMembershipForm()

    if form.validate_on_submit():
        session.execute(text("""
            CALL UpdateAvailableMembership(:membership_id, :type, :price, :description, :hascoach)
        """), {
            'membership_id': membership_id,
            'type': form.type.data,
            'price': form.price.data,
            'description': form.description.data,
            'hascoach': form.hascoach.data
        })
        session.commit()
        session.close()

        return redirect(url_for('.manage_memberships'))
    return render_template('edit_membership.html', form=form, membership=membership)

def delete_membership_route(membership_id, db, app):
    admin_engine = db.get_engine(app, bind='admin')
    Session = sessionmaker(bind=admin_engine)
    session = Session()

    session.execute(text("""CALL DeleteAvailableMembership(:membership_id)
    """), {'membership_id': membership_id})
    session.commit()
    session.close()

    return redirect(url_for('.manage_memberships'))