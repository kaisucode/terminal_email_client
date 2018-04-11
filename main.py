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

msg = MIMEMultipart()



def indexOf(list1, piece): 
    return -1 if piece not in list1 else list1.index(piece)

def addFile(user_input): 
    aelin_email_location = os.getcwd()
    add_cwd = -1

    # Absolute locations
    # ~/Desktop/file.txt
    # /home/kevin/Desktop/file.txt
    # ~/Downloads/..Desktop

    # Add cwd first
    # ../file.txt
    # file.txt

    slash_index = user_input.rfind('/')
    if slash_index != -1: 
        filename = user_input[slash_index+1:]
        if user_input[:2] == "../": 
            add_cwd = 1
        else: 
            add_cwd = 0
    else: 
        filename = user_input
        add_cwd = 1

    if add_cwd == 1: 
        file_path = aelin_email_location+'/'+user_input
    else: 
        file_path = user_input


    #  filename = "NAME OF THE FILE WITH ITS EXTENSION"
    attachment = open(file_path, "rb")
     
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
     
    msg.attach(part)





fromaddr = "kevinlegobuilder@gmail.com"
toaddr = "kevinlegobuilder@gmail.com"
 
 
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Sent from aelin_email"


#  if "-f" in message: 
#      File go from "-f" index to "-m" or "" or end
#      Message go from -m to end or the entire ""
    
#  if "-m" in message: 
#      Go from -m to end

#  if no parameters in message: 
#      Message go from start to end 


message_indicator_Index = indexOf(sys.argv, "-m")
#  file_indicator_Index = indexOf(sys.argv, "-f")
#  quotaion_indicator_Index = indexOfQuote(sys.argv, "\"")





# if -m added
if (message_indicator_Index != -1): 
    aelin_email_message = " ".join(sys.argv[message_indicator_Index+1:])
else: 
    aelin_email_message = sys.argv[-1]
    message_indicator_Index = len(sys.argv)-1

body = aelin_email_message



# Attach files
if sys.argv[1] == "-f" and len(sys.argv) == 3: 
    addFile(sys.argv[2])
    body = ""
elif sys.argv[1] == "-f": 
    for i in range(2, message_indicator_Index): 
        addFile(sys.argv[i])
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





