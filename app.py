from flask import Flask, Blueprint
from flask_login import LoginManager, login_required
from flask_sqlalchemy import SQLAlchemy
import os
from routes.admin_dashboard_routes import dashboard_route
from routes.admin_manage_coaches_routes import edit_coaches_route, manage_coaches_route, delete_coach_route
from routes.admin_manage_memberships_routes import manage_memberships_route, edit_membership_route, delete_membership_route
from routes.auth_routes import login_route, register_route
from routes.user_routes import home_route, memberships_route, coaches_route, payments_route, logout_route
from services.data_obtainer import load_user_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://public_user_account:p5rICIDxj0@localhost/gym'
app.config['SQLALCHEMY_BINDS'] = {
    'admin': 'postgresql://admin_user:SK23rKv0zf@localhost/gym'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = './static/img'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET'])
def dashboard():
    return dashboard_route(db, app)

@admin_bp.route('/manage-memberships', methods=['GET', 'POST'])
def manage_memberships():
    return manage_memberships_route(db, app)


@admin_bp.route('/edit-membership/<membership_id>', methods=['GET', 'POST'])
def edit_membership(membership_id):
    return edit_membership_route(membership_id, db, app)


@admin_bp.route('/delete-membership/<uuid:membership_id>', methods=['GET','POST'])
def delete_membership(membership_id):
    return delete_membership_route(membership_id, db, app)


@admin_bp.route('/manage-coaches', methods=['GET', 'POST'])
def manage_coaches():
    return manage_coaches_route(db, app)


@admin_bp.route('/edit-coach/<coach_id>', methods=['GET', 'POST'])
def edit_coach(coach_id):
    return edit_coaches_route(coach_id, db, app)

@admin_bp.route('/delete-coach/<coach_id>', methods=['GET', 'POST'])
def delete_coach(coach_id):
    return delete_coach_route(coach_id, db, app)

app.register_blueprint(admin_bp, url_prefix='/admin')

@login_manager.user_loader
def load_user(member_id):
    return load_user_data(member_id, db)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_route(db)

@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_route(db)

@app.route('/', methods=['GET','POST'])
@login_required
def home():
    return home_route(db)


@app.route('/memberships', methods=['GET', 'POST'])
@login_required
def memberships():
    return memberships_route(db)

@app.route('/coaches')
@login_required
def coaches():
    return coaches_route(db)

@app.route('/payments', methods=['GET', 'POST'])
@login_required
def payments():
    return payments_route(db)

@app.route('/logout')
@login_required
def logout():
    return logout_route()

if __name__ == '__main__':
    app.run(debug=True)
