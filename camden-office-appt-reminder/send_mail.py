# ############################################## #
#    To automatically check for pending email    #
#        reminders in conjunction with the       #
#               scheduling software.             #
#                                                #
#          Copyright 2007 Daniel Ralston         #
# ############################################## #
import smtplib
import datetime

def send_message(company, sender, sender_email, password, recipient_email, recipient, year, month, day, time): 
        day_of_week = {
            "1": "Monday",
            "2": "Tuesday",
            "3": "Wednesday",
            "4": "Thursday",
            "5":"Friday",
            "6": "Saturday",
            "7": "Sunday"
            }
        weekday = datetime.date(int(year), int(month), int(day)).weekday()
        date = str(day_of_week[str(weekday+1)]+", "+str(month)+"/"+str(day)+"/"+str(year))
        if time.endswith("pm"):
            print_time = time
            pass
        else:
            print_time = time+" am"
        subject = "Upcoming Appointment"
        
        message = "Hello, "+recipient+",\n  This is an automated reminder that you have an appointment at "+company+" at "+print_time+" on, "+date+". If you have recieved this message in error, please inform your therapist as soon as possible. If you need to reschedule or cancel, please provide at least a 24 hour notice.\nThanks!\n     "+company
        
        headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, recipient, subject)
        reminder = headers + message

        mailserver = smtplib.SMTP("smtp.gmail.com", 587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login("JRandomUser@gmail.com", "password")
        mailserver.sendmail("JRandomUser@gmail.com", recipient_email, reminder)
        mailserver.close()
        return 0
