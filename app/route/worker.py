# app/routes/worker.py
from flask import Blueprint
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pytz
import smtplib
import traceback
from app import app, db
from app.models import Todo, User

worker_bp = Blueprint('worker', __name__)

@worker_bp.route("/run-email-worker")
def run_email_worker():
    india_tz = pytz.timezone("Asia/Kolkata")
    now = datetime.now(india_tz)
    todos = Todo.query.filter_by(notified=False).all()

    for todo in todos:
        if todo.planned_date and todo.planned_time:
            planned_dt = india_tz.localize(datetime.combine(todo.planned_date, todo.planned_time))
            reminder_dt = planned_dt - timedelta(minutes=5)
            delta = (reminder_dt - now).total_seconds()
            if 0 <= delta <= 60:
                user = User.query.filter_by(id=todo.user_id).first()
                if user:
                    try:
                        msg = MIMEMultipart()
                        msg['From'] = app.config['MAIL_USERNAME']
                        msg['To'] = user.email
                        msg['Subject'] = "Todo Reminder: 5 Minutes Left"
                        msg.attach(MIMEText(
                            f"Hi {user.username},\n\nThis is a reminder for your Todo:\n\n"
                            f"Title: {todo.title}\nDescription: {todo.desc}\n\n- MyTodo App", 'plain'))
                        with smtplib.SMTP_SSL(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as server:
                            server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                            server.sendmail(msg['From'], msg['To'], msg.as_string())
                        todo.notified = True
                        db.session.commit()
                        print(f"[INFO] Email sent to {user.email} for Todo: {todo.title}")
                    except Exception as e:
                        print(f"[ERROR] Email failed: {e}")
                        traceback.print_exc()
    return "Email worker triggered!", 200
