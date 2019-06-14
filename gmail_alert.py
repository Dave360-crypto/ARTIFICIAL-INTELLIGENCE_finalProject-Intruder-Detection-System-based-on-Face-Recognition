import smtplib

gmail_user = 'testnetworkmonitor@gmail.com'  
gmail_password = 'testnetworkmonitortestnetworkmonitor'

sent_from = gmail_user  
to = ['justkeepcool10@gmail.com', 'faisalsmkaf@gmail.com']  
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
