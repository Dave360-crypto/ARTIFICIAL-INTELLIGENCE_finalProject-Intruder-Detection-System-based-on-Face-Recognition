import smtplib

gmail_user = 'user@gmail.com'  
gmail_password = 'userpassword'

sent_from = gmail_user  
to = ['receiver1@gmail.com', 'receiver2@gmail.com']  
subject = 'Intruder detect'  
body = 'Hey, whats up?\n\n- You'

email_text = """\  
From: %s  
To: %s  
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:  
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print ('Email alert sent from script!')
except:  
    print ('Something went wrong...')
