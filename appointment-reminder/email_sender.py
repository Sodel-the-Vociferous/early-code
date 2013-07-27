# ############################################## #
#    To automatically check for pending email    #
#        reminders in conjunction with the       #
#               scheduling software.             #
#                                                #
#          Copyright 2007 Daniel Ralston         #
# ############################################## #
import smtplib
import datetime

def send_message(company, FROM, recipient_email, recipient, year, month, appt_day, appt_time): 
    day_of_week = {
        "1": "Monday",
        "2": "Tuesday",
        "3": "Wednesday",
        "4": "Thursday",
        "5":"Friday",
        "6": "Saturday",
        "7": "Sunday"
        }
    sender = "eagle.mountain.massage@gmail.com"
    day = datetime.date(int(year), int(month), int(appt_day)).weekday()
    func_date = day_of_week[str(day+1)]+", "+str(month)+"/"+str(appt_day)+"/"+str(year)
    date = str(func_date)
    if appt_time.endswith("p"):
        print_time = appt_time.strip("p")
        print_time = time+" p.m."
    else:
        print_time = appt_time+" a.m."
    subject = "Test smtplib"
    
    message = "Hello, "+recipient+",\n  This is an automated reminder that you have an appointment at "+company+" at "+print_time+" on, "+date+". If you need to reschedule or cancel, please provide at least a 24 hour notice.\nThanks!\n     "+company+"\n\n---------------------------------------------------------------------\nThis email address is not monitored. If you need to contact "+company+", send your message to \'lgralston@shaw.ca\'."

    headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, recipient, subject)
    reminder = headers + message

    mailserver = smtplib.SMTP("smtp.gmail.com", 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login("eagle.mountain.massage@gmail.com", "applesauce")
    mailserver.sendmail("eagle.mountain.massage@gmail.com", "lgralston@shaw.ca", reminder)
    mailserver.close()