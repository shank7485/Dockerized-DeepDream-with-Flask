import glob
import os
import Queue
import thread
import json

import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

waiting_list = Queue.Queue()
gmail_user = ""
gmail_pwd = ""

#Mails to user.
def mail(to, subject, text, attach):
    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['to'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
    msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    mailServer.close()


#Gets path of newly added item in the given path.
def find_newly_added(path):
    newest = max(glob.iglob(path + '*.jpg'), key=os.path.getctime)
    return newest

#Keeps adding newly added files into folder into Queue. Pops the queue and runs thread.
def inputs_folder_checker(newest):
        while(True):
            temp = find_newly_added("/opt/deepdream/outputs/")
            if newest != temp:
                newest = temp
                waiting_list.put(newest)
                file_path = waiting_list.get()
		print file_path
                file_name = (file_path.split("/")[-1]).split(".")[0] #Gives name of image.
                thread.start_new_thread(mailer, (file_path, find_user_emailID(file_name), ))

#Finds email ID of user by querying JSON file keyed at userID
def find_user_emailID(userID):
    with open('userData.json', 'r') as user_jsonfile:
            data = json.load(user_jsonfile)
    return data[userID]

#Mails to user the new photo.
def mailer(user_photo, user_emailID):
    print "Mailing" + user_photo
    mail(user_emailID, "Photo from Deep Dream", "Please find attached photo", user_photo)
    print "Mailed " + user_photo +" to "+ user_emailID

inputs_folder_checker("/opt/deepdream/outputs/")
