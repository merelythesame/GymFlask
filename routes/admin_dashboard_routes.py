import matplotlib.pyplot as plt
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from flask import render_template


def plot_bar_chart(x, y, xlabel, ylabel, title, filename, colors=None):
    plt.bar(x, y, color=colors)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(f'./static/img/{filename}.png')
    plt.close()


def plot_line_chart(x, y, xlabel, ylabel, title, filename):
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='b', label='Revenue Line')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(range(1, 13), labels=[str(i) for i in range(1, 13)])
    plt.grid(True)
    plt.savefig(f'./static/img/{filename}.png')
    plt.close()


def fetch_data_from_db(session, query):
    return session.execute(text(query)).fetchall()


def get_db_session(db, app):
    admin_engine = db.get_engine(app, bind='admin')
    Session = sessionmaker(bind=admin_engine)
    return Session()


def dashboard_route(db, app):
    session = get_db_session(db, app)

    active_membership_counts = fetch_data_from_db(session, "SELECT * FROM ActiveMembershipCounts")
    monthly_revenue = fetch_data_from_db(session, "SELECT * FROM MonthlyRevenue")
    active_member_coach_status = fetch_data_from_db(session, "SELECT * FROM ActiveMemberCoachStatus")
    payment_type_counts = fetch_data_from_db(session, "SELECT * FROM PaymentTypeCounts")

    if active_membership_counts:
        membership_types = [item[0] for item in active_membership_counts]
        counts = [item[1] for item in active_membership_counts]
        plot_bar_chart(membership_types, counts, 'Тип абонементу', 'Кількість', 'Кількість активних абонементів',
                       'ActiveMembershipCounts')

    if monthly_revenue:
        months = [item[0].month for item in monthly_revenue]
        total_revenue = [float(item[1]) for item in monthly_revenue]
        plot_line_chart(months, total_revenue, 'Місяць', 'Дохід', 'Місячний дохід', 'MonthlyRevenue')

    if active_member_coach_status:
        coach_status = [item[0] for item in active_member_coach_status]
        counts = [item[1] for item in active_member_coach_status]
        plot_bar_chart(coach_status, counts, 'Статус', 'Кількість користувачів',
                       'Кількість активних користувачів з тренером', 'ActiveMemberCoachStatus',
                       colors=['orange', 'green'])

    if payment_type_counts:
        payment_types = [item[0] for item in payment_type_counts]
        counts = [item[1] for item in payment_type_counts]
        plot_bar_chart(payment_types, counts, 'Тип платежу', 'Кількість платежів', 'Популярні типи попвнень',
                       'PaymentTypeCounts', colors=['blue', 'green', 'orange'])

    session.close()
    return render_template('admin_home.html')
