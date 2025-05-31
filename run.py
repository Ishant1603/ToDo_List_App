from app import app, db
from app.models import Todo, User
import threading
import time
from datetime import datetime, timedelta
import pytz
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_worker import email_notification_worker 
import traceback

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
       # print("[INFO] Starting background email worker...")
        threading.Thread(target=email_notification_worker, daemon=True).start()
        app.run(debug=True)
