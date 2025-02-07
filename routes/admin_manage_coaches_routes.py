import os
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from flask import render_template, redirect, url_for
from werkzeug.utils import secure_filename
from services.forms import CoachForm
from services.data_obtainer import get_all_coaches


def handle_photo_upload(photo_file, app, current_photo=None):
    if photo_file:
        filename = secure_filename(photo_file.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo_file.save(photo_path)
        return os.path.basename(photo_path)
    return current_photo


def get_db_session(db, app):
    admin_engine = db.get_engine(app, bind='admin')
    Session = sessionmaker(bind=admin_engine)
    return Session()


def execute_db_query(session, query, params=None, fetch_one=False, fetch_all=False):
    result = session.execute(text(query), params or {})

    if fetch_one:
        return result.fetchone()
    if fetch_all:
        return result.fetchall()

    session.commit()


def manage_coaches_route(db, app):
    form = CoachForm()
    coaches = get_all_coaches(db)

    if form.validate_on_submit():
        photo_path = handle_photo_upload(form.photo.data, app)

        session = get_db_session(db, app)
        execute_db_query(session, """CALL InsertCoach(:name, :lastName, :speciality, :phoneNumber, :photo)""", {
            'name': form.name.data,
            'lastName': form.lastName.data,
            'speciality': form.speciality.data,
            'phoneNumber': form.phoneNumber.data,
            'photo': photo_path
        })
        session.close()

        return redirect(url_for('admin.manage_coaches'))

    return render_template('manage_coaches.html', form=form, coaches=coaches)


def edit_coaches_route(coach_id, db, app):
    session = get_db_session(db, app)

    raw_coach = execute_db_query(session, """SELECT * FROM Coaches WHERE coachId = :coach_id""",
                                 {'coach_id': coach_id}, fetch_one=True)

    if not raw_coach:
        return redirect(url_for('admin.manage_coaches'))

    coach = {
        'coachid': str(raw_coach.coachid),
        'name': raw_coach.name,
        'lastName': raw_coach.lastname,
        'speciality': raw_coach.speciality,
        'phoneNumber': raw_coach.phonenumber,
        'photo': raw_coach.photo
    }

    form = CoachForm(obj=coach)

    if form.validate_on_submit():
        photo_path = handle_photo_upload(form.photo.data, app, coach['photo'])

        execute_db_query(session, """CALL UpdateCoach(:coach_id, :name, :last_name, :speciality, :phone_number, :photo)""", {
            'coach_id': coach_id,
            'name': form.name.data,
            'last_name': form.lastName.data,
            'speciality': form.speciality.data,
            'phone_number': form.phoneNumber.data,
            'photo': photo_path
        })
        session.close()

        return redirect(url_for('admin.manage_coaches'))

    session.close()
    return render_template('edit_coach.html', form=form, coach=coach)



def delete_coach_route(coach_id, db, app):
    session = get_db_session(db, app)

    execute_db_query(session, """CALL DeleteCoach(:coach_id)""", {'coach_id': coach_id})
    session.close()

    return redirect(url_for('admin.manage_coaches'))
