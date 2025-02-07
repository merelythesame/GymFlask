from sqlalchemy.sql import text

class UserService:
    def __init__(self, db):
        self.db = db

    def execute_db_query(self, query, params=None, fetch_one=False, fetch_all=False, commit=False):
        session = self.db.session
        try:
            result = session.execute(text(query), params or {})

            if fetch_one:
                return result.fetchone()
            if fetch_all:
                return result.fetchall()
            if commit:
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_user_by_phone_number(self, phone_number):
        return self.execute_db_query("SELECT * FROM Members WHERE phoneNumber = :phoneNumber;",
                                     {'phoneNumber': phone_number}, fetch_one=True)

    def get_user_details_by_id(self, member_id):
        return self.execute_db_query("SELECT * FROM getmemberdetailsbyid(:member_id);",
                                     {'member_id': member_id}, fetch_one=True)

    def insert_user(self, form, hashed_password):
        return self.execute_db_query("""CALL InsertUser(:name, :surname, :phone, :password, :membershipId, :balance)""",
                                     {
                                         'name': form.name.data,
                                         'surname': form.last_name.data,
                                         'phone': form.phone_number.data,
                                         'password': hashed_password,
                                         'membershipId': None,
                                         'balance': 0.00
                                     }, commit=True)

    def process_deposit(self, amount, payment_type, user_id):
        self.execute_db_query("CALL deposit(:id, :amount, :type)",
                              {'id': user_id, 'amount': amount, 'type': payment_type}, commit=True)

    def change_password(self, user_id, old_password, new_password, current_password_hash):
        from werkzeug.security import check_password_hash, generate_password_hash

        if not check_password_hash(current_password_hash, old_password):
            return False

        hashed_password = generate_password_hash(new_password, method='scrypt')
        self.execute_db_query("CALL EditUserPassword(:userId, :newPassword)",
                              {'userId': user_id, 'newPassword': hashed_password}, commit=True)
        return True

    def assign_membership_to_member(self, membership_id, member_id, coach_id=None):
        query = "CALL AssignMembershipToMember(:userId, :membership_id" + (", :coach_id" if coach_id else "") + ")"
        params = {'userId': member_id, 'membership_id': membership_id}

        if coach_id:
            params['coach_id'] = coach_id

        self.execute_db_query(query, params, commit=True)