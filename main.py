import os
import sys

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#  from commands.execute import execute

import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG, format='DEBUG: %(message)s')
logging.getLogger().disabled = True


aelin_email_location = os.getcwd()


fromaddr = "kevinlegobuilder@gmail.com"
toaddr = "kevinlegobuilder@gmail.com"
 
msg = MIMEMultipart()
 
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Sent from aelin_email"


haveMessage = 0


message_indicator_Index = -1 if "-m" not in sys.argv else sys.argv.index("-m")
file_indicator_Index = -1 if "-m" not in sys.argv else sys.argv.index("-f")

# if -m added
if (message_indicator_Index != -1): 
    aelin_email_message = " ".join(sys.argv[message_indicator_Index+1:])
else: 
    aelin_email_message = sys.argv[-1]
    message_indicator_Index = len(sys.argv)-1

body = aelin_email_message



# Attach files
if sys.argv[1] == "-f": 
    for i in range(2, message_indicator_Index): 

        add_cwd = -1

        # Absolute locations
        # ~/Desktop/file.txt
        # /home/kevin/Desktop/file.txt
        # ~/Downloads/..Desktop

        # Add cwd first
        # ../file.txt
        # file.txt

        slash_index = sys.argv[i].rfind('/')
        if slash_index != -1: 
            filename = sys.argv[i][slash_index+1:]
            if sys.argv[i][:2] == "../": 
                add_cwd = 1
            else: 
                add_cwd = 0
        else: 
            filename = sys.argv[i]
            add_cwd = 1

        if add_cwd == 1: 
            file_path = aelin_email_location+'/'+sys.argv[i]
        else: 
            file_path = sys.argv[i]


        #  filename = "NAME OF THE FILE WITH ITS EXTENSION"
        attachment = open(file_path, "rb")
         
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
         
        msg.attach(part)
elif len(sys.argv) > 2: 
    print("Add '-f' to send files")
    exit()
 




 
 
msg.attach(MIMEText(body, 'plain'))
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "theaureatehades")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()





