#!/usr/bin/env python

# ############################## #
#     (C)2007 Daniel Ralston     #
# Appointment Reminder Software  #
#                                #
#          callback.py           #
# ############################## #

import shelve
import sys
import calendar
import sys
import time
import datetime
import os
import send_mail

internal = True

class Database:
#Provides a central storage unit to keep track of any and all our data
    def __init__(self):
        self.appointments = {}
        self.clients = {}
        self.preferences = {"save at close": True,
                            "send reminders": True, 
                            "send at login": True,
                            "company": "",
                            "email": ""}
        self.possible_times = { 1:"7:00",
                                2:"7:15",
                                3:"7:30",
                                4:"7:45",
                                5:"8:00",
                                6:"8:15",
                                7:"8:30",
                                8:"8:45",
                                9:"9:00",
                                10:"9:15",
                                11:"9:30",
                                12:"9:45",
                                13:"10:00",
                                14:"10:15",
                                15:"10:30",
                                16:"10:45",
                                17:"11:00",
                                18:"11:15",
                                19:"11:30",
                                20:"11:45",
                                21:"12:00pm",
                                22:"12:15pm",
                                23:"12:30pm",
                                24:"12:45pm",
                                25:"1:00pm",
                                26:"1:15pm",
                                27:"1:30pm",
                                28:"1:45pm",
                                29:"2:00pm",
                                30:"2:15pm",
                                31:"2:30pm",
                                32:"2:45pm",
                                33:"3:00pm",
                                34:"3:15pm",
                                35:"3:30pm",
                                36:"3:45pm",
                                37:"4:00pm",
                                38:"4:15pm",
                                39:"4:30pm",
                                40:"4:45pm",
                                41:"5:00pm",
                                42:"5:15pm",
                                43:"5:30pm",
                                44:"5:45pm",
                                45:"6:00pm",
                                46:"6:15pm",
                                47:"6:30pm",
                                48:"6:45pm",
                                49:"7:00pm",
                                50:"7:15pm",
                                51:"7:30pm",
                                52:"7:45pm",
                                53:"8:00pm",
                                54:"8:15pm",
                                55:"8:30pm",
                                56:"8:45pm",
                                57:"9:00pm"}
        self.day_names = {1: "Monday",
                          2: "Tuesday",
                          3: "Wednesday",
                          4: "Thursday",
                          5: "Friday",
                          6: "Saturday",
                          7: "Sunday"}
        self.current_user = ""
        self.close_program = False
    def new_appointment(self, year, month, day, time, length, email, email_bool, client, notes = None, force = False): 
#                        length is the length in minutes divided by 15
        if client != "":
            if force == True:
                if (year, month, day, time) in database.appointments:
                    database.remove_appointment(year, month, day, time) 
            if (year, month, day, time) not in self.appointments:
                i = 1
                exists = 0
                while i < length:
                    if (year, month, day, time+i) not in self.appointments:
                        pass
                    else:
                        error_handler.error(None, "Prior Appointment Exists In Specified Time Range")
                        return 1
                    i = i + 1
                
                else:
                    self.appointments[(year, month, day, time)] = Appointment(year, month, day, time, length, email, email_bool, client, notes)
                    i = 1
                    while (i < length) and (time + i in self.possible_times):
                        self.appointments[(year, month, day, time + i)] = client
                        i = i + 1
                    return 0
            else:
                error_handler.error(None, "Prior Appointment Exists In Specified Timeslot")
                return 1
    def remove_appointment(self, year, month, day, time):
        #where time is the length of the appointment divided by 15(minutes)
        if (year, month, day, time) in self.appointments:
            length = self.appointments[(year, month, day, time)].length
            del self.appointments[(year, month, day, time)]
            i = 1
            while (i < length) and (time + i in self.possible_times):
                del self.appointments[(year, month, day, time + i)]
                i = i + 1
        else:
            print "yo"
            error_handler.error(None, "No Appointment At Specified Timeslot")
        return
    def new_client(self, name, email, email_bool, notes = None, force = False):
        if name not in self.clients:
            self.clients[name] = name
            self.clients[name] = Client(name, email, email_bool)
        else:
            if force == False:
                error_handler.error(None, "Client Of That Name In Record")
            else:
                del self.clients[name]
                self.new_client(name, email, email_bool, notes)
        return
    def remove_client(self, widget, name):
        appts = self.appointments
        if name in self.clients:
            del self.clients[name]
            for entry in appts:
                if self.appointments[entry].client == name:
                    del self.appointments[entry]
        return
    def save_data(self, widget = None, user = None):
        preferences = shelve.open("preferences")
        key_base = shelve.open("key_base")
        appointments = shelve.open("appointments")
        clients = shelve.open("clients")
        
        for i in key_base:
            del key_base[i]
        for i in appointments:
            del appointments[i]
        for i in preferences:
            del preferences[i]
        for i in self.preferences:
            preferences[i] = self.preferences[i]
        for i in clients:
            del clients[i]
        for i in self.clients:
            clients[i] = self.clients[i]
        iteration = 0
        for i in self.appointments:
            appointments[str(iteration)] = self.appointments[i]
            key_base[str(iteration)] = i
            iteration = iteration + 1
        appointments.close()
        clients.close()
        preferences.close()
        return
    def get_data(self, widget = None, user = None):
        preferences = shelve.open("preferences")
        appointments = shelve.open("appointments")
        key_base = shelve.open("key_base")
        clients = shelve.open("clients")
        
        for i in preferences:
            self.preferences[i] = preferences[i]
        for i in clients:
            self.clients[i] = clients[i]
        iteration = 0
        for i in appointments:
            if appointments[str(iteration)] != "":
                self.appointments[key_base[str(iteration)]] = appointments[str(iteration)]
                iteration = iteration + 1
        appointments.close()
        clients.close()
        preferences.close()
        return
class Client:
    def __init__(self, name, email, email_bool, notes = None):
        self.name = name
        self.email = email
        self.email_bool = email_bool
        notes = []
        if notes != None:
            for i in notes:
                self.notes.append(notes[i]) #Special notes can be added easily
        
class Appointment:
    def __init__(self, year, month, day, time, length, email, email_bool, client, auto_blocked = 0, notes = None):
        self.year = year
        self.month = month
        self.day = day
        self.time = time
        self.length = length
        self.email = email
        self.email_bool = email_bool
        self.client = client
        self.auto_blocked = auto_blocked
        self.notes = []
        self.sent = False
        if notes != None:
            for i in notes:
                self.notes.append(notes[i])
class Error_Handler:
    def error(self, widget = None, message = None, type = "ok", positive = None, negative = None, parameter1 = None, parameter2 = None, size_x = 320, size_y = 200, prev_window = None):
        #Error "hub" where the appropraite dialogs are dispatched from.
        #"positive" is the appropriate function to call if the type is "yes/no", and the anser is affirmative
        #"parameter1" is the "positive" function's parameter
        #"negative" and "parameter2"hold the call if the type is "yes/no", and the answer is negative
        if prev_window != None:
            prev_window.hide_all()
        self.error_window = gtk.Window()
        self.error_window.set_title('Error')
        self.error_window.set_border_width(5)
        self.error_window.connect("destroy", self.destroy_error_dialog, prev_window)
        self.error_window.set_resizable(False)
        
        error_box = gtk.VBox(False, 10)
        error_box.set_size_request(size_x, size_y)
        self.error_window.add(error_box)

        error_box.add(gtk.Label(message))
        if type == "ok":
            ok_button = gtk.Button("OK")
            ok_button.connect("clicked", self.destroy_error_dialog)
            error_box.add(ok_button)
        elif type == "yes/no":
            prev_window.hide_all()
            yes_button = gtk.Button("Okay")
            error_box.add(yes_button)
            no_button = gtk.Button("Cancel")
            error_box.add(no_button)
            if positive != None:
                yes_button.connect("clicked", self.exec_positive, prev_window, positive, parameter1)
            if negative != None:
                no_button.connect("clicked", negative, parameter2)
        self.error_window.show_all()
    def destroy_error_dialog(self, widget =  None, prev_window = None):
        if prev_window != None:
            prev_window.show_all()
        self.error_window.destroy()          
        pass
    def exec_positive(self, widget, prev_window, positive, parameter1):
        if prev_window != None:
            prev_window.show_all()
        self.destroy_error_dialog
        positive(None, parameter1)
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        self.time = time
    def increment_days(self, days):
        if (days >= 0):
            target_year = self.year
            #print target_year
            target_month = self.month
            #print target_month
            target_day = self.day
            #print target_day
            month_length = self.month_length(self.month, self.year)
            #print month_length, "len"
            iterations = 0
            while (iterations < days):
                if target_day == month_length:
                    target_day = 1
                    #print target_day, "day"
                    target_month = self.increment_month()[0]
                    #print target_month, "month"
                    target_year = self.increment_month()[1]
                    #print target_year, "year"
                    iterations = iterations + 1
                    #print iterations, "\n"
                else:
                    target_day = target_day + 1
                    #print target_day, "Tag"
                    #print target_month, "month#"
                    #print target_year, "Jahre"
                    iterations = iterations + 1
                    #print iterations, "\n"
            return (target_year, target_month, target_day)
        else:            
            error_handler.error("increment_days(self, days): Error, negative input")
    def increment_month(self, months = 1):
        if months >= 0:
            if self.month == 12:
                return (1, self.year + 1)
            else:
                return (self.month + 1, self.year)
        else:
            error_handler.error("increment_months(self.months): Error, negative input")
    def month_length(self, month, year):
        if month == 1:
            return 31
        elif month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 28
            else:
                return 29
        elif month == 3:
            return 31
        elif month == 4:
            return 30
        elif month == 5:
            return 31
        elif month == 6:
            return 30
        elif month == 7:
            return 31
        elif month == 8:
            return 31
        elif month == 9:
            return 30
        elif month == 10:
            return 31
        elif month == 11:
            return 30
        elif month == 12:
            return 31
class Sender:
    def get_today(self):
        year, month, day, a, b, c, d, e, f = time.localtime()
        return year, month, day
    def query(self):
        print ("Querying...")
        for year, month, day, time in database.appointments:
            if str(type(database.appointments[year, month, day, time])) !="<type \'str\'>":
                if database.appointments[year, month, day, time].sent == False:                            
                    if database.appointments[year, month, day, time].email_bool == True:
                        company = database.preferences["company"]
                        sender = database.current_user
                        sender_email = "eagle.mountain.massage@gmail.com"
                        password = "password"
                                
                        recipient_name = database.appointments[year, month, day, time].client
                        recipient_email = database.clients[recipient_name].email
                        
                        for i in database.possible_times:
                            ntime = database.possible_times[time]
                            if i == time:
                                time = i
                        if send_mail.send_message(company, sender, sender_email, password, recipient_email, recipient_name, year, month, day, ntime) == 0:
                            database.appointments[year, month, day, time].sent = True
                            print ("Sent message to "+recipient_name+" for appointment "+str(year)+", "+str(month)+", "+str(day)+str(time))
                        else:
                            print ("Error sending message to "+recipient_name+" for appointment "+str(year)+", "+str(month)+", "+str(day)+str(ntime))
if __name__ == "__main__":
    yn = ""
    print "This program automatically checks for pending e-mail reminders."
    print "Do you want to send pending e-mails now?"
    yn = str(raw_input("[y/n]>"))
    if yn == "y":
        error_handler = Error_Handler()
        database = Database()
        today = Sender().get_today()
        database.current_user = "JRandomUser"
        os.chdir((str(sys.path[0])+"/databases/"+"JRandomUser"))
        database.get_data()
        Sender().query()
        database.save_data(user = database.current_user)
    elif yn == "n":
        print "Closing..."
    else:
        print "Unrecognized Command.\nClosing..."