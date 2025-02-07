from flask import render_template
from services.AdminService import AdminService


def dashboard_route(db, app):
    admin_service = AdminService(db, app)
    session = admin_service.get_db_session()

    active_membership_counts = admin_service.execute_db_query("SELECT * FROM ActiveMembershipCounts", fetch_all=True)
    monthly_revenue = admin_service.execute_db_query("SELECT * FROM MonthlyRevenue", fetch_all=True)
    active_member_coach_status = admin_service.execute_db_query("SELECT * FROM ActiveMemberCoachStatus", fetch_all=True)
    payment_type_counts = admin_service.execute_db_query("SELECT * FROM PaymentTypeCounts", fetch_all=True)

    if active_membership_counts:
        membership_types = [item[0] for item in active_membership_counts]
        counts = [item[1] for item in active_membership_counts]
        admin_service.plot_bar_chart(membership_types, counts, 'Тип абонементу', 'Кількість', 'Кількість активних абонементів',
                       'ActiveMembershipCounts')

    if monthly_revenue:
        months = [item[0].month for item in monthly_revenue]
        total_revenue = [float(item[1]) for item in monthly_revenue]
        admin_service.plot_line_chart(months, total_revenue, 'Місяць', 'Дохід', 'Місячний дохід', 'MonthlyRevenue')

    if active_member_coach_status:
        coach_status = [item[0] for item in active_member_coach_status]
        counts = [item[1] for item in active_member_coach_status]
        admin_service.plot_bar_chart(coach_status, counts, 'Статус', 'Кількість користувачів',
                       'Кількість активних користувачів з тренером', 'ActiveMemberCoachStatus',
                       colors=['orange', 'green'])

    if payment_type_counts:
        payment_types = [item[0] for item in payment_type_counts]
        counts = [item[1] for item in payment_type_counts]
        admin_service.plot_bar_chart(payment_types, counts, 'Тип платежу', 'Кількість платежів', 'Популярні типи попвнень',
                       'PaymentTypeCounts', colors=['blue', 'green', 'orange'])

    session.close()
    return render_template('admin_home.html')
