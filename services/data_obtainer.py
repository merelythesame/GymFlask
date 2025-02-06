from flask_login import UserMixin
from sqlalchemy.sql import text

class Member(UserMixin):
    def __init__(self, member_id, name, surname, phone, balance, membership_end_date, membership_type, membership_id, coach_full_name, password):
        self.member_id = member_id
        self.name = name
        self.surname = surname
        self.phone = phone
        self.balance = balance
        self.membership_end_date = membership_end_date
        self.membership_type = membership_type
        self.membership_id = membership_id
        self.coach_full_name = coach_full_name
        self.password = password

    def get_id(self):
        return str(self.member_id)

    def __repr__(self):
        return f'<Member {self.name} {self.surname}>'


def load_user_data(member_id, db):
    if member_id is None:
        print(None)

    result = db.session.execute(
        text("SELECT * FROM getmemberdetailsbyid(:member_id);"),
        {'member_id': member_id}
    ).fetchone()
    if result:
        return Member(
            member_id=result.member_id,
            name=result.member_name,
            surname=result.member_surname,
            phone=result.member_phone,
            balance=result.balance,
            membership_end_date=result.membership_enddate,
            membership_type=result.membership_type,
            membership_id=result.membershipid,
            coach_full_name=result.coach_full_name,
            password = result.password
        )
    return None

def get_all_available_memberships(db):
    result = db.session.execute(text("SELECT * FROM availablememberships;")).fetchall()

    available_memberships = []
    if result:
        for row in result:
            available_memberships.append({
                'membershipid': str(row.membershipid),
                'type': row.type,
                'price': float(row.price),
                'description': row.description,
                'hascoach': bool(row.hascoach)
            })
    return available_memberships

def get_all_coaches_to_pick(db):
    result = db.session.execute(text("SELECT * FROM allcoachespick;")).fetchall()
    coaches_to_pick = []
    if result:
        for row in result:
            coaches_to_pick.append((str(row.coachid), row.fullname))
    return coaches_to_pick

def get_all_coaches(db):
    result = db.session.execute(text("SELECT * FROM Coaches;")).fetchall()
    coaches = []
    if result:
        for row in result:
            coaches.append({
                'coachid': str(row.coachid),
                'fullname': row.name + ' ' +  row.lastname,
                'speciality': row.speciality,
                'phonenumber': row.phonenumber,
                'photo': row.photo
            })
    return coaches