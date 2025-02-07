import os
import matplotlib.pyplot as plt
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename

class AdminService:
    def __init__(self, db, app):
        self.db = db
        self.app = app

    def get_db_session(self):
        admin_engine = self.db.get_engine(self.app, bind='admin')
        Session = sessionmaker(bind=admin_engine)
        return Session()

    def execute_db_query(self, query, params=None, fetch_one=False, fetch_all=False):
        session = self.get_db_session()
        result = session.execute(text(query), params or {})

        if fetch_one:
            return result.fetchone()
        if fetch_all:
            return result.fetchall()

        session.commit()
        session.close()

    def plot_bar_chart(self, x, y, xlabel, ylabel, title, filename, colors=None):
        plt.bar(x, y, color=colors)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.savefig(f'./static/img/{filename}.png')
        plt.close()

    def plot_line_chart(self, x, y, xlabel, ylabel, title, filename):
        plt.figure(figsize=(8, 6))
        plt.plot(x, y, marker='o', linestyle='-', color='b', label='Revenue Line')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(range(1, 13), labels=[str(i) for i in range(1, 13)])
        plt.grid(True)
        plt.savefig(f'./static/img/{filename}.png')
        plt.close()

    def handle_photo_upload(self, photo_file, current_photo=None):
        if photo_file:
            filename = secure_filename(photo_file.filename)
            photo_path = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
            photo_file.save(photo_path)
            return os.path.basename(photo_path)
        return current_photo