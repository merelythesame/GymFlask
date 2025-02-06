import matplotlib.pyplot as plt
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from flask import render_template


def dashboard_route(db, app):
    admin_engine = db.get_engine(app, bind='admin')
    Session = sessionmaker(bind=admin_engine)
    session = Session()

    active_membership_counts_query = session.execute(text("SELECT * FROM ActiveMembershipCounts"))
    monthly_revenue_query = session.execute(text("SELECT * FROM MonthlyRevenue"))
    active_member_coach_status_query = session.execute(text("SELECT * FROM ActiveMemberCoachStatus"))
    payment_type_counts_query = session.execute(text("SELECT * FROM PaymentTypeCounts"))

    active_membership_counts = active_membership_counts_query.fetchall()
    if active_membership_counts:
        membership_types = [item[0] for item in active_membership_counts]
        counts = [item[1] for item in active_membership_counts]

        plt.bar(membership_types, counts)
        plt.xlabel('Тип абонементу')
        plt.ylabel('Кількість')
        plt.title('Кількість активних абонементів')

        plt.savefig(f'./static/img/ActiveMembershipCounts.png')
        plt.close()
    else:
        print("No active membership data to plot.")


    monthly_revenue = monthly_revenue_query.fetchall()
    if monthly_revenue:
        months = [item[0].month for item in monthly_revenue]
        total_revenue = [float(item[1]) for item in monthly_revenue]

        plt.figure(figsize=(8, 6))

        plt.plot(months, total_revenue, marker='o', linestyle='-', color='b', label='Revenue Line')

        plt.xlabel('Місяць')
        plt.ylabel('Дохід')
        plt.title('Місячний дохід')

        plt.xticks(range(1, 13), labels=[str(i) for i in range(1, 13)])

        plt.grid(True)

        plt.savefig(f'./static/img/MonthlyRevenue.png')
        plt.close()
    else:
        print("No monthly revenue data to plot.")

    active_member_coach_status = active_member_coach_status_query.fetchall()
    if active_member_coach_status:
        coach_status = [item[0] for item in active_member_coach_status]
        counts = [item[1] for item in active_member_coach_status]

        plt.figure(figsize=(8, 6))

        plt.bar(coach_status, counts, color=['orange', 'green'])

        plt.xlabel('Статус')
        plt.ylabel('Кількість користувачів')
        plt.title('Кількість активних користувачів з тренером')

        plt.savefig(f'./static/img/ActiveMemberCoachStatus.png')
        plt.close()
    else:
        print("No active member coach status data to plot.")

    payment_type_counts = payment_type_counts_query.fetchall()
    if payment_type_counts:
        payment_types = [item[0] for item in payment_type_counts]
        counts = [item[1] for item in payment_type_counts]

        plt.figure(figsize=(8, 6))
        plt.bar(payment_types, counts, color=['blue', 'green', 'orange'])

        plt.xlabel('Тип платежу')
        plt.ylabel('Кількість платежів')
        plt.title('Популярні типи попвнень')

        plt.savefig(f'./static/img/PaymentTypeCounts.png')
        plt.close()
    else:
        print("No payment type data to plot.")

    session.close()

    return render_template('admin_home.html')
