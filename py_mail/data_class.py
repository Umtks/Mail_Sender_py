import csv
import datetime
import shutil
import os
from tempfile import NamedTemporaryFile
from utils.templates import get_template, render_context
from smtplib import SMTP
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

host = "smtp.gmail.com"
port = 587
username = "******"  #your mail adress
password = "*****" #your password
from_email = username
to_list = ["testertest128d@gmail.com"]

#file_item_path = os.path.join(os.getcwd(), "data.csv")
file_item_path = os.path.join(os.path.dirname(__file__), "data.csv")




class UserManager():

    def render_message(self, user_data):
        file_ = "templates\email_messages.txt"  
        file_html = "templates\email_messages.html"
        template = get_template(file_)
        template_html = get_template(file_html)
        if isinstance(user_data, dict):
            context = user_data
            plain_ = render_context(template, context)
            html_ = render_context(template_html, context)
            return (plain_, html_)
        return (None, None)


    def message_user(self ,user_id=None, email=None, subject= "Bill information!"):
        user = self.get_user_data(user_id=user_id, email=email)
        if user:
            try:
                plain_, html_ = self.render_message(user)
                print(plain_, html_)
                user_email = user.get("email", "testertest128d@gmail.com")
                to_list.append(user_email)
                email_conn = SMTP(host, port)
                email_conn.ehlo()
                email_conn.starttls()
                email_conn.login(username, password)
                the_msg = MIMEMultipart("alternative")
                the_msg["Subject"] = subject
                the_msg["From"] = from_email
                the_msg["To"] = user_email
                part_1 = MIMEText(plain_, "plain")
                part_2 = MIMEText(html_, "html")
                the_msg.attach(part_1) 
                the_msg.attach(part_2)
                email_conn.sendmail(from_email, to_list, the_msg.as_string())
                email_conn.quit()
            except smtplib.SMTPException:
                    print("error")
        return None    



    def get_user_data(self, user_id=None, email=None):
        filename = file_item_path
        print(file_item_path)
        with open(filename,"r") as csvfile:
            reader = csv.DictReader(csvfile)
            items = []
            unknown_user_id = None
            unknown_email = None

            for row in reader:
                if user_id is not None:
                    if int(user_id) == int(row.get("id")):
                        return row
                    else:
                        unknown_user_id = user_id    
                if email is not None:
                    if email == row.get("email"):
                        return row
                    else:
                         unknown_email = email      