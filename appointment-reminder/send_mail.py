#!/usr/bin/env python

# ############################## #
#     (C)2007 Daniel Ralston     #
# Appointment Reminder Software  #
#                                #
#          callback.py           #
# ############################## #

import time
import time as time_op
import shelve
import sys
import email_sender
import time as mtime

data_indexes = {}
class Appointment:#Creates a template for appointments
    def __init__(self, appt_year, appt_month, appt_day, appt_time, bool_email, client):
        self.my_year = appt_year
        self.my_month = appt_month
        self.my_day = appt_day
        self.my_time = appt_time
        self.my_client = client
    def change_client(self):
         self.my_client = new_client_name
         appointments[(appt_year, appt_month, appt_day, appt_time)] = new_client_name
class Client:
    def __init__(self, f_name, l_name, email_addr):
        self.f_name = f_name
        self.l_name = l_name
        self.name = f_name+" "+l_name
        self.name = str(self.name)
        self.email = email_addr
    def alter_name(self):
        self.name = new_client_name
    def alter_email(self):
        self.email = new_client_email
class Data:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self.appointments = {}
        self.clients = {}
def number_of_days(month, year):
    month = month - 1
    if month == 0:
        return 31
    if month == 1:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return 28
        else:
            return 29
    elif month ==  2:
        return 31
    elif month == 3:
        return 30
    elif month == 4:
        return 31
    elif month == 5:
        return 30
    elif month == 6:
        return 31
    elif month == 7:
        return 31
    elif month == 8:
        return 30
    elif month == 9:
        return 31
    elif month == 10:
        return 30
    elif month == 11:
        return 31
def increment_date(year, month, day, increment_iterations):
    month_length = number_of_days(month, day)
    func_day = day
    func_month = month
    func_year = year
    if increment_iterations > 0:
        iteration = 0
        func_day = day
        func_month = month
        func_year = year
        while iteration < increment_iterations:
            iteration = iteration + 1
            if day == month_length:
                if month == 12:
                    func_day = 1
                    func_month = 1
                    func_year = func_year + 1
                else:
                    func_day = 1
                    func_month = func_month + 1
            else:
                func_day = func_day + 1
    target_day.year = func_year
    target_day.month = func_month
    target_day.day = func_day
    return
def get_data():
    client_data = shelve.open('ClientData')#Opens the main client list
    appt_data = shelve.open('ApptData')
    database = shelve.open('Database')
    for name in client_data:
        data_container.clients[name] = client_data[name]
    for key in database:
        data_container.appointments[database[key]]=appt_data[key]
    client_data.close()
    appt_data.close()
    database.close()
    return
def get_now():
    year, month, day, a, b, c, d, e, f = time.localtime()
    return year, month, day
def queue():
    print "querying pending reminders for", target_day.year, target_day.month, target_day.day, "..."
    for year, month, day, time in data_container.appointments:
        if year == target_day.year:
            if month == target_day.month:
                if day == target_day.day:
                    try:
                        email_sender.send_message("Eagle Mountain Massage Therapy",
                                                  "eagle.mountain.massage@gmail.com", 
                                                  data_container.clients[data_container.appointments[year, month, day, time].my_client].email, 
                                                  data_container.appointments[year, month, day, time].my_client, 
                                                  target_day.year, 
                                                  target_day.month, 
                                                  target_day.day, 
                                                  time)
                        print "Message sent to", data_container.clients[data_container.appointments[year, month, day, time].my_client].email, "successfully.\n"
                    except:
                        print "Message send to", data_container.clients[data_container.appointments[year, month, day, time].my_client].email, "for", target_day.month, target_day.day, target_day.year, "failed."
                        print "Please check email address validity, and contact your internet service provider if problem persists."
    mtime.sleep(5)
def main():
    time == 30
    print "This program automatically checks for pending e-mail reminders."
    print "Do you want to send pending e-mails now?"
    yn = str(raw_input("[y/n]>"))
    if yn == "y":
        #data_indexes["primary": target_day]
        #data_indexes["secondary": data_container]
        get_data()
        increment_date(data_container.year, data_container.month, data_container.day, 2)
        print
        queue()
    elif yn == "n":
        sys.exit
    else:
        print "Bad command"
        print "\n\n\n\n"
        main()
if __name__ == "__main__":
    year, month, day = get_now()
    data_container = Data(year, month, day)
    target_day = Data(year, month, day)
    main()