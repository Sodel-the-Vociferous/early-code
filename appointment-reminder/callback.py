#!/usr/bin/env python

# ############################## #
#     (C)2007 Daniel Ralston     #
# Appointment Reminder Software  #
#                                #
#          callback.py           #
# ############################## #

import sys
import shelve
import pygtk
pygtk.require('2.0')
import gtk, pango
import time
import datetime
import calendar as cal

#------------------------------Global Variables------------------------------#

bool_auto_backup = 1
appointments = {}
callable_times = {}
by_day_times = {}
clients = {}
bynumber = {}
new_client_name = ""
new_client_email = ""
new_appt_time = ""
my_times = [
        "7:00",
        "7:15",
        "7:30",
        "7:45",
        "8:00",
        "8:15",
        "8:30",
        "8:45",
        "9:00",
        "9:15",
        "9:30",
        "9:45",
        "10:00",
        "10:15",
        "10:30",
        "10:45",
        "11:00",
        "11:15",
        "11:30",
        "11:45",
        "12:00p",
        "12:15p",
        "12:30p",
        "12:45p",
        "1:00p",
        "1:15p",
        "1:30p",
        "1:45p",
        "2:00p",
        "2:15p",
        "2:30p",
        "2:45p",
        "3:00p",
        "3:15p",
        "3:30p",
        "3:45p",
        "4:00p",
        "4:15p",
        "4:30p",
        "4:45p",
        "5:00p",
        "5:15p",
        "5:30p",
        "5:45p",
        "6:00p",
        "6:15p",
        "6:30p",
        "6:45p",
        "7:00p",
        "7:15p",
        "7:30p",
        "7:45p",
        "8:00p",
        "8:15p",
        "8:30p",
        "8:45p",
        "9:00p"
        ]
day_of_week = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
        ]
            
#-----------------------------Class  Definitions-----------------------------#

class Appointment:#Creates a template for appointments
    def __init__(self, appt_year, appt_month, appt_day, appt_time, bool_email, client):
        self.my_year = appt_year
        self.my_month = appt_month
        self.my_day = appt_day
        self.my_time = appt_time
        self.my_client = client
class Client:#Creates a template for clients
    def __init__(self, f_name, l_name, email_addr):
        self.f_name = f_name
        self.l_name = l_name
        self.name = f_name+" "+l_name
        self.name = str(self.name)
        self.email = email_addr
#------------------------------Global Functions------------------------------#
def increment_day(year, month, day, increment_iterations):
    #To return a date a certain number of days in the future.
    #Inputs: (a)year, (b)month, (c)day, (d)number of days to increment by
    #Outputs: Original date incremented by d
    month_length = number_of_days(month, day)
    if increment_iterations > 0:
        iteration = 0
        while iteration < increment_iterations:
            iteration = iteration + 1
            if day == month_length:
                if month == 12:
                    target_day.day = 1
                    target_day.month = 1
                    target_day.year = year + 1
                else:
                    target_day.day = 1
                    target_day.month = month + 1
            else:
                target_day.day = day+1
    return
def decrement_day(year, month, day, decrement_iterations):
    #To return a date a certain number of days in the past.
    #Inputs: (a)year, (b)month, (c)day, (d)number of days to decrement by
    #Outputs: Original date decremented by d
    if decrement_iterations > 0:
        iteration = 0
        while iteration < decrement_iterations:
            iteration = iteration + 1
            if day != 1:
                day = day - 1
            elif day == 1:
                if month == 0:
                    month = 11
                    year = year - 1
                    day = 31
                else:
                    month = month - 1
                    if month == 1:
                        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                            day = 28
                        else:
                            day = 28
                    elif month ==  2:
                        day = 31
                    elif month == 3:
                        day = 30
                    elif month == 4:
                        day = 31
                    elif month == 5:
                        day = 30
                    elif month == 6:
                        day = 31
                    elif month == 7:
                        day = 31
                    elif month == 8:
                        day = 30
                    elif month == 9:
                        day = 31
                    elif month == 10:
                        day = 30
                    elif month == 11:
                        day = 31
        else:
            return
    return
def number_of_days(month, year):
    #To return the number of days in a given month
    #Inputs: (a)month, (b)year
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
def new_appointment(appt_year, appt_month, appt_day, appt_time, email_bool, the_client):
    #To automate adding a new appointment to the list
    #Inputs: (a)year, (b)month, (c)day, (d)time, (e)whether or not to send automatic email reminders, (f)the client to mak the appointment for
    appointments[(appt_year, appt_month, appt_day, appt_time)] = the_client
    appointments[(appt_year, appt_month, appt_day, appt_time)] = Appointment(appt_year, appt_month, appt_day, appt_time, email_bool, the_client)
def save_data(self):
    #To save the client and appointment data
    client_data = shelve.open('ClientData')#Opens the main client list
    appt_data = shelve.open('ApptData')
    database = shelve.open('Database')
    for name in client_data:
        del client_data[name]
    for name in clients:
        try:
            del client_data[name]
        except:
            pass
        client_data[name] = clients[name]
    client_data.close()
    i = 0
    for date in appointments:
        if appointments[date].my_client!= "":
            i=i+1
            database[str(i)]=date
            appt_data[str(i)]=appointments[date]
    client_data.close()
    appt_data.close()
    database.close()
    print "\nSaved!\n"
def get_data():
    #To retrieve client and appointment data
    client_data = shelve.open('ClientData')#Opens the main client list
    appt_data = shelve.open('ApptData')
    database = shelve.open('Database')
    for name in client_data:
        clients[name] = client_data[name]
        print "imported:", clients[name].name
    for key in database:
        appointments[database[key]]=appt_data[key]
    client_data.close()
    appt_data.close()
    database.close()
#--------------------------------Main  Window--------------------------------#
class MainWindow:
    DEF_NONE = 0
    DEF_PAD = 10
    DEF_PAD_SMALL = 5
    TM_YEAR_BASE = 1900
    
    def about_popup(self, widget):
        #To create an "about" popup window
        self.about = gtk.Window()
        self.about.set_title('About')
        self.about.set_border_width(5)
        self.about.connect("destroy", self.about_destroy)
        self.about.show()
        self.about.set_resizable(False)
       
        about_frame = gtk.Frame("")
        self.about.add(about_frame)
        about_frame.show()
        about_text = gtk.Label("Copyright 2008 Daniel Ralston\nversion 0.8")
        about_text.show()
        about_frame.add(about_text)
    def about_destroy(self, widget):
        #Destroy the "about" window
        self.about.destroy()
    def dummy(self, widget):
        #Does nothing if a function is syntactically required
        pass
    def new_client(self, client_name, f_name, l_name, client_email):
        #To automate adding a new client to the client list
        #Inputs: (a)full name, (b)first name, (c)last name, (d)client's email address
        if client_name not in (" ", "", "   "):
            if client_name not in clients:
                clients[client_name] = client_name
                clients[client_name] = Client(f_name, l_name, client_email)
                self.client_select.append_text(client_name)
                self.f_name.set_text("New client created")
                self.l_name.set_text("")
                self.e_mail.set_text("")
                self.days_info()
        elif client_name in clients:
            self.f_name.set_text("That name is already a client")
        else:
            self.f_name.set_text("Field Required")
            self.l_name.set_text("Field Required")
    def remove_client(self, widget):
        #To automate removing a client from the client list. This method requires updating the GUI in several ares.
        model = self.client_select.get_model()
        index = self.client_select.get_active()
        self.selected_client = model[index][0]
        name = model[index][0]
        print "deleting", name
        self.client_select.remove_text(index)
        self.client_select.set_active(-1)
        del clients[self.selected_client] 
        self.selector_box.remove(self.client_select)
        self.client_select = gtk.combo_box_new_text()
        self.selector_box.add(self.client_select)
        self.client_select.show()
        for entry in clients:
            self.client_select.append_text(clients[entry].name)
        self.client_select.connect("changed", self.cb_changed)
        self.display_f_name.set_text("Client Removed!")
        self.display_l_name.set_text("Client Removed!")
        self.display_e_mail.set_text("Client Removed!")
        func_appts = appointments.copy()
        for entry in func_appts:
            if func_appts[entry].my_client == name:
                del appointments[entry]
        for entry in clients:
            print clients[entry].name
        self.days_info()
        
    def calendar_date_to_string(self):
        #To return the monday of the week of the current day selected in the calendar view
        year, month, day = self.window.get_date()
        while datetime.date(year, month+1, day).weekday() != 0:
            if day != 1:
                day = day - 1
            elif day == 1:
                if month == 0:
                    month = 11
                    year = year - 1
                    day = 31
                else:
                    month = month - 1
                    if month == 1:
                        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                            day = 28
                        else:
                            day = 28
                    elif month ==  2:
                        day = 31
                    elif month == 3:
                        day = 30
                    elif month == 4:
                        day = 31
                    elif month == 5:
                        day = 30
                    elif month == 6:
                        day = 31
                    elif month == 7:
                        day = 31
                    elif month == 8:
                        day = 30
                    elif month == 9:
                        day = 31
                    elif month == 10:
                        day = 30
                    elif month == 11:
                        day = 31
            #print "I have iterated\n"
        mytime = time.mktime((year, month+1, day, 0, 0, 0, 0, 0, -1))
        #print year, month+1, day
        self.cal_day = day
        self.cal_month = month+1
        self.cal_year = year        
        
        self.days_info()
        
        #print self.cal_year, self.cal_month, self.cal_day
        return time.strftime("%x", time.localtime(mytime))
    def days_info(self):
        #To update the week view
        self.window.freeze()
        func_day = self.cal_day
        func_month = self.cal_month
        func_year = self.cal_year
        
        #Monday
         #Set Monday's date values so we can work with them
        self.monday_day = func_day
        self.monday_month = func_month
        self.monday_year = func_year
        self.cal_monday_date = "Monday, "+str(func_year)+", "+str(func_month)+", "+str(func_day)
        
        #Tuesday
         #Set Tuesday's date values so we can work with them.
        self.tuesday_day = func_day + 1 #Tuesday's default date is one day after Monday. If we need to change it, we will do so with the following code
        self.tuesday_month = func_month #Tuesday's default month is the same as Monday's
        self.tuesday_year = func_year #Same with the year
        
        if func_day == number_of_days(func_month, func_year): #If monday was the last day of the month
            self.tuesday_day = 1  #Tuesday is the first day of the month
            if func_month == 12: #If Monday's month was December
                self.tuesday_month = 1 #It will now be January
                self.tuesday_year = func_year + 1 #It will now be one year up
            else: #If it wasn't December
                self.tuesday_month = func_month + 1 #It is one month above Monday's month
            self.cal_tuesday_date = "Tuesday, "+str(self.tuesday_year)+", "+str(self.tuesday_month)+", "+str(self.tuesday_day)#Set Tuesday's date label for the Week View
        else: #If monday was nothing special
            self.cal_tuesday_date = "Tuesday, "+str(self.tuesday_year)+", "+str(self.tuesday_month)+", "+str(self.tuesday_day)#Tuesday is one day after monday
        
        #Wednesday
        self.wednesday_day = self.tuesday_day + 1
        self.wednesday_month = self.tuesday_month
        self.wednesday_year = self.tuesday_year
        if self.tuesday_day == number_of_days(self.tuesday_month, self.tuesday_year):
            self.wednesday_day = 1
            if self.tuesday_month == 12:
                self.wednesday_month = 1
                self.wednesday_year = self.tuesday_year + 1
            else:
                self.wednesday_month = func_month + 1
            self.cal_wednesday_date = "Wednesday, "+str(self.wednesday_year)+", "+str(self.wednesday_month)+", "+str(self.wednesday_day)
        else:
            self.cal_wednesday_date = "Wednesday, "+str(self.wednesday_year)+", "+str(self.wednesday_month)+", "+str(self.wednesday_day)        
        #Thursday
        self.thursday_day = self.wednesday_day + 1
        self.thursday_month = self.wednesday_month
        self.thursday_year = self.wednesday_year
        if self.wednesday_day == number_of_days(self.wednesday_month, self.wednesday_year):
            self.thursday_day = 1
            if self.wednesday_month == 12:
                self.thursday_month = 1
                self.thursday_year = self.wednesday_year + 1
            else:
               self. thursday_month = func_month + 1
            self.cal_thursday_date = "Thursday, "+str(self.thursday_year)+", "+str(self.thursday_month)+", "+str(self.thursday_day)
        else:
           self. cal_thursday_date = "Thursday, "+str(self.thursday_year)+", "+str(self.thursday_month)+", "+str(self.thursday_day)
        
        #Friday
        self.friday_day = self.thursday_day + 1
        self.friday_month = self.thursday_month
        self.friday_year = self.thursday_year
        if self.thursday_day == number_of_days(self.wednesday_month, self.wednesday_year):
            self.friday_day = 1
            if self.thursday_month == 12:
                self.friday_month = 1
                self.friday_year = self.thursday_year + 1
            else:
                self.friday_month = func_month + 1
            self.cal_friday_date = "Friday, "+str(self.friday_year)+", "+str(self.friday_month)+", "+str(self.friday_day)
        else:
            self.cal_friday_date = "Friday, "+str(self.friday_year)+", "+str(self.friday_month)+", "+str(self.friday_day)
        
        #Saturday
        self.saturday_day = self.friday_day + 1
        self.saturday_month = self.friday_month
        self.saturday_year = self.friday_year
        if self.friday_day == number_of_days(self.wednesday_month, self.wednesday_year):
            self.saturday_day = 1
            if self.friday_month == 12:
                self.saturday_month = 1
                self.saturday_year = func_year + 1
            else:
                self.saturday_month = self.friday_month + 1
            self.cal_saturday_date = "Saturday, "+str(self.saturday_year)+", "+str(self.saturday_month)+", "+str(self.saturday_day)
        else:
            self.cal_saturday_date = "Saturday, "+str(self.saturday_year)+", "+str(self.saturday_month)+", "+str(self.saturday_day)
        
        #Sunday
        self.sunday_day = self.saturday_day + 1
        self.sunday_month = self.saturday_month
        self.sunday_year = self.saturday_year
        if self.saturday_day == number_of_days(self.wednesday_month, self.wednesday_year):
            self.sunday_day = 1
            if self.saturday_month == 12:
                self.sunday_month = 1
                self.sunday_year = self.saturday_year + 1
            else:
                self.sunday_month = func_month + 1
            self.cal_sunday_date = "Sunday, "+str(self.sunday_year)+", "+str(self.sunday_month)+", "+str(self.sunday_day)
        else:
            self.cal_sunday_date = "Sunday, "+str(self.sunday_year)+", "+str(self.sunday_month)+", "+str(self.sunday_day)
        
        self.monday_frame.set_label(self.cal_monday_date)
        #print self.cal_monday_date, "1\n"
        self.tuesday_frame.set_label(self.cal_tuesday_date)
        self.wednesday_frame.set_label(self.cal_wednesday_date)
        self.thursday_frame.set_label(self.cal_thursday_date)
        self.friday_frame.set_label(self.cal_friday_date)
        #print self.cal_friday_date, "1\n"
        self.saturday_frame.set_label(self.cal_saturday_date)
        self.sunday_frame.set_label(self.cal_sunday_date)
        
        #Monday
        self.monday_frame.remove(self.monday_display_day)
        del self.monday_display_day
        self.monday_display_day = gtk.VBox(False, self.DEF_PAD)
        self.monday_frame.add(self.monday_display_day)
        self.monday_display_day.show()
        for time in my_times:
            time_frame = gtk.Frame(time)
            time_frame.show()
            self.monday_display_day.add(time_frame)
            time_box = gtk.VBox(False, self.DEF_PAD_SMALL)
            time_box.set_size_request(200, 25)
            time_box.show()
            time_frame.add(time_box)
            mclient_selector = gtk.combo_box_new_text()
            mclient_selector.connect("changed", self.set_appointment_mon, time)
            time_box.add(mclient_selector)
            mclient_selector.show()
            for (year, month, day, my_time) in appointments:
                if year == self.monday_year:
                    if month == self.monday_month:
                        if day == self.monday_day:
                            if my_time == time:
                                if (year, month, day, time) in appointments:
                                    mclient_selector.insert_text(0, appointments[self.monday_year, self.monday_month, self.monday_day, time].my_client)
            mclient_selector.append_text("")
            for entry in clients:
                if (self.monday_year, self.monday_month, self.monday_day, time) in appointments:
                    if entry != appointments[self.monday_year, self.monday_month, self.monday_day, time].my_client:
                        mclient_selector.append_text(clients[entry].name)
                else:
                    mclient_selector.append_text(clients[entry].name)
            mclient_selector.set_active(0)
        #Tuesday
        self.tuesday_frame.remove(self.tuesday_display_day)
        del self.tuesday_display_day
        self.tuesday_display_day = gtk.VBox(False, self.DEF_PAD)
        self.tuesday_frame.add(self.tuesday_display_day)
        self.tuesday_display_day.show()
        for time in my_times:
            time_frame = gtk.Frame(time)
            time_frame.show()
            self.tuesday_display_day.add(time_frame)
            time_box = gtk.VBox(False, self.DEF_PAD_SMALL)
            time_box.set_size_request(200, 25)
            time_box.show()
            time_frame.add(time_box)
            client_selector = gtk.combo_box_new_text()
            client_selector.connect("changed", self.set_appointment_tue, time)
            time_box.add(client_selector)
            client_selector.show()
            for (year, month, day, my_time) in appointments:
                if year == self.tuesday_year:
                    if month == self.tuesday_month:
                        if day == self.tuesday_day:
                            if my_time == time:
                                if (year, month, day, time) in appointments:
                                    client_selector.insert_text(0, appointments[self.tuesday_year, self.tuesday_month, self.tuesday_day, time].my_client)
            client_selector.append_text("")
            for entry in clients:
                if (self.tuesday_year, self.tuesday_month, self.tuesday_day, time) in appointments:
                    if entry != appointments[self.tuesday_year, self.tuesday_month, self.tuesday_day, time].my_client:
                        client_selector.append_text(clients[entry].name)
                else:
                    client_selector.append_text(clients[entry].name)
            client_selector.set_active(0)
        #Wednesday
        self.wednesday_frame.remove(self.wednesday_display_day)
        del self.wednesday_display_day
        self.wednesday_display_day = gtk.VBox(False, self.DEF_PAD)
        self.wednesday_frame.add(self.wednesday_display_day)
        self.wednesday_display_day.show()
        for time in my_times:
            time_frame = gtk.Frame(time)
            time_frame.show()
            self.wednesday_display_day.add(time_frame)
            time_box = gtk.VBox(False, self.DEF_PAD_SMALL)
            time_box.set_size_request(200, 25)
            time_box.show()
            time_frame.add(time_box)
            client_selector = gtk.combo_box_new_text()
            client_selector.connect("changed", self.set_appointment_wed, time)
            time_box.add(client_selector)
            client_selector.show()
            for (year, month, day, my_time) in appointments:
                if year == self.wednesday_year:
                    if month == self.wednesday_month:
                        if day == self.wednesday_day:
                            if my_time == time:
                                if (year, month, day, time) in appointments:
                                    client_selector.insert_text(0, appointments[self.wednesday_year, self.wednesday_month, self.wednesday_day, time].my_client)
            client_selector.append_text("")
            for entry in clients:
                if (self.wednesday_year, self.wednesday_month, self.wednesday_day, time) in appointments:
                    if entry != appointments[self.wednesday_year, self.wednesday_month, self.wednesday_day, time].my_client:
                        client_selector.append_text(clients[entry].name)
                else:
                    client_selector.append_text(clients[entry].name)
            client_selector.set_active(0)
        #Thursday
        self.thursday_frame.remove(self.thursday_display_day)
        del self.thursday_display_day
        self.thursday_display_day = gtk.VBox(False, self.DEF_PAD)
        self.thursday_frame.add(self.thursday_display_day)
        self.thursday_display_day.show()
        for time in my_times:
            time_frame = gtk.Frame(time)
            time_frame.show()
            self.thursday_display_day.add(time_frame)
            time_box = gtk.VBox(False, self.DEF_PAD_SMALL)
            time_box.set_size_request(200, 25)
            time_box.show()
            time_frame.add(time_box)
            client_selector = gtk.combo_box_new_text()
            client_selector.connect("changed", self.set_appointment_thu, time)
            time_box.add(client_selector)
            client_selector.show()
            for (year, month, day, my_time) in appointments:
                if year == self.thursday_year:
                    if month == self.thursday_month:
                        if day == self.thursday_day:
                            if my_time == time:
                                if (year, month, day, time) in appointments:
                                    client_selector.insert_text(0, appointments[self.thursday_year, self.thursday_month, self.thursday_day, time].my_client)
            client_selector.append_text("")
            for entry in clients:
                if (self.thursday_year, self.thursday_month, self.thursday_day, time) in appointments:
                    if entry != appointments[self.thursday_year, self.thursday_month, self.thursday_day, time].my_client:
                        client_selector.append_text(clients[entry].name)
                else:
                    client_selector.append_text(clients[entry].name)
            client_selector.set_active(0)
        #Friday
        self.friday_frame.remove(self.friday_display_day)
        del self.friday_display_day
        self.friday_display_day = gtk.VBox(False, self.DEF_PAD)
        self.friday_frame.add(self.friday_display_day)
        self.friday_display_day.show()
        for time in my_times:
            time_frame = gtk.Frame(time)
            time_frame.show()
            self.friday_display_day.add(time_frame)
            time_box = gtk.VBox(False, self.DEF_PAD_SMALL)
            time_box.set_size_request(200, 25)
            time_box.show()
            time_frame.add(time_box)
            client_selector = gtk.combo_box_new_text()
            client_selector.connect("changed", self.set_appointment_fri, time)
            time_box.add(client_selector)
            client_selector.show()
            for (year, month, day, my_time) in appointments:
                if year == self.friday_year:
                    if month == self.friday_month:
                        if day == self.friday_day:
                            if my_time == time:
                                if (year, month, day, time) in appointments:
                                    client_selector.insert_text(0, appointments[self.friday_year, self.friday_month, self.friday_day, time].my_client)
            client_selector.append_text("")
            for entry in clients:
                if (self.friday_year, self.friday_month, self.friday_day, time) in appointments:
                    if entry != appointments[self.friday_year, self.friday_month, self.friday_day, time].my_client:
                        client_selector.append_text(clients[entry].name)
                else:
                    client_selector.append_text(clients[entry].name)
            client_selector.set_active(0)
        #Saturday
        self.saturday_frame.remove(self.saturday_display_day)
        del self.saturday_display_day
        self.saturday_display_day = gtk.VBox(False, self.DEF_PAD)
        self.saturday_frame.add(self.saturday_display_day)
        self.saturday_display_day.show()
        for time in my_times:
            time_frame = gtk.Frame(time)
            time_frame.show()
            self.saturday_display_day.add(time_frame)
            time_box = gtk.VBox(False, self.DEF_PAD_SMALL)
            time_box.set_size_request(200, 25)
            time_box.show()
            time_frame.add(time_box)
            client_selector = gtk.combo_box_new_text()
            client_selector.connect("changed", self.set_appointment_fri, time)
            time_box.add(client_selector)
            client_selector.show()
            for (year, month, day, my_time) in appointments:
                if year == self.saturday_year:
                    if month == self.saturday_month:
                        if day == self.saturday_day:
                            if my_time == time:
                                if (year, month, day, time) in appointments:
                                    client_selector.insert_text(0, appointments[self.saturday_year, self.saturday_month, self.saturday_day, time].my_client)
            client_selector.append_text("")
            for entry in clients:
                if (self.saturday_year, self.saturday_month, self.saturday_day, time) in appointments:
                    if entry != appointments[self.saturday_year, self.saturday_month, self.saturday_day, time].my_client:
                        client_selector.append_text(clients[entry].name)
                else:
                    client_selector.append_text(clients[entry].name)
            client_selector.set_active(0)
        #Sunday
        self.sunday_frame.remove(self.sunday_display_day)
        del self.sunday_display_day
        self.sunday_display_day = gtk.VBox(False, self.DEF_PAD)
        self.sunday_frame.add(self.sunday_display_day)
        self.sunday_display_day.show()
        for time in my_times:
            time_frame = gtk.Frame(time)
            time_frame.show()
            self.sunday_display_day.add(time_frame)
            time_box = gtk.VBox(False, self.DEF_PAD_SMALL)
            time_box.set_size_request(200, 25)
            time_box.show()
            time_frame.add(time_box)
            client_selector = gtk.combo_box_new_text()
            client_selector.connect("changed", self.set_appointment_fri, time)
            time_box.add(client_selector)
            client_selector.show()
            for (year, month, day, my_time) in appointments:
                if year == self.sunday_year:
                    if month == self.sunday_month:
                        if day == self.sunday_day:
                            if my_time == time:
                                if (year, month, day, time) in appointments:
                                    client_selector.insert_text(0, appointments[self.sunday_year, self.sunday_month, self.sunday_day, time].my_client)
            client_selector.append_text("")
            for entry in clients:
                if (self.sunday_year, self.sunday_month, self.sunday_day, time) in appointments:
                    if entry != appointments[self.sunday_year, self.sunday_month, self.sunday_day, time].my_client:
                        client_selector.append_text(clients[entry].name)
                else:
                    client_selector.append_text(clients[entry].name)
            client_selector.set_active(0)
        self.window.freeze()
    def calendar_set_signal_strings(self, sig_str):
        pass

    def calendar_month_changed(self, widget):
        buffer = "month_changed: %s" % self.calendar_date_to_string()
        self.calendar_set_signal_strings(buffer)

    def calendar_day_selected(self, widget):
        buffer = self.calendar_date_to_string()
        self.calendar_set_signal_strings(buffer)

    def calendar_prev_month(self, widget):
        buffer = "prev_month: %s" % self.calendar_date_to_string()
        self.calendar_set_signal_strings(buffer)

    def calendar_next_month(self, widget):
        buffer = "next_month: %s" % self.calendar_date_to_string()
        self.calendar_set_signal_strings(buffer)

    def calendar_prev_year(self, widget):
        buffer = "prev_year: %s" % self.calendar_date_to_string()
        self.calendar_set_signal_strings(buffer)

    def calendar_next_year(self, widget):
        buffer = "next_year: %s" % self.calendar_date_to_string()
        self.calendar_set_signal_strings(buffer)

    def set_appointment_mon(self, combobox, time):
        #To create an appointment for the selected monday form the information from a given time's multi-box
        #print self.monday_month, "Thismonth\n"
        model = combobox.get_model()
        index = combobox.get_active()
        if model[index][0]!="":
            new_appointment(self.monday_year, self.monday_month, self.monday_day, time, 1, model[index][0])
        
    def set_appointment_tue(self, combobox, time):
        #print self.tuesday_month, "Thismonth"
        model = combobox.get_model()
        index = combobox.get_active()
        if model[index][0]!="":
            new_appointment(self.tuesday_year, self.tuesday_month, self.tuesday_day, time, 1, model[index][0])
        
    def set_appointment_wed(self, combobox, time):
        model = combobox.get_model()
        index = combobox.get_active()
        if model[index][0]!="":
            new_appointment(self.wednesday_year, self.wednesday_month, self.wednesday_day, time, 1, model[index][0])
        
    def set_appointment_thu(self, combobox, time):
        model = combobox.get_model()
        index = combobox.get_active()
        if model[index][0]!="":
            new_appointment(self.thursday_year, self.thursday_month, self.thursday_day, time, 1, model[index][0])
        
    def set_appointment_fri(self, combobox, time):
        model = combobox.get_model()
        index = combobox.get_active()
        if model[index][0]!="":
            new_appointment(self.friday_year, self.friday_month, self.friday_day, time, 1, model[index][0])

    def set_appointment_sat(self, combobox, time):
        model = combobox.get_model()
        index = combobox.get_active()
        if model[index][0]!="":
            new_appointment(self.saturday_year, self.saturday_month, self.saturday_day, time, 1, model[index][0])
        
    def set_appointment_sun(self, combobox, time):
        model = combobox.get_model()
        index = combobox.get_active()
        if model[index][0]!="":
            new_appointment(self.sunday_year, self.sunday_month, self.sunday_day, time, 1, model[index][0])
        
    def cb_changed(self, combobox):
        #To change the selected client in the lient management window
        model = combobox.get_model()
        index = combobox.get_active()
        if index != -1:
            self.selected_client = model[index][0]
            self.display_f_name.set_text(clients[model[index][0]].f_name)
            self.display_l_name.set_text(clients[model[index][0]].l_name)
            self.display_e_mail.set_text(clients[model[index][0]].email)
        return
    
    def make_new_client(self, make_client):
        #Creates a new client based on the fields entered into the client creation window
        client_name = self.f_name.get_text()+" "+self.l_name.get_text()
        self.new_client(client_name, self.f_name.get_text(), self.l_name.get_text(), self.e_mail.get_text())
        
    def change_l_name_begin(self, widget):
        #First half of processes required to change the client's first name in the client management window
        l_name = self.display_l_name.get_text()
        self.old_l_name=self.display_l_name.get_text()
        self.old_name = self.display_f_name.get_text()+" "+l_name
        self.selector_box.remove(self.client_select)
        self.client_select = gtk.combo_box_new_text()
        self.selector_box.add(self.client_select)
        self.client_select.append_text(self.old_name)
        self.client_select.connect("changed", self.dummy)
        if l_name not in ("", " "):
            self.l_name_box.remove(self.display_l_name)
            self.l_name_box.remove(self.change_l_name)
            del self.display_l_name
            del self.change_l_name
            self.change_name_entry = gtk.Entry(max=0)
            self.change_name_entry.set_text(l_name)
            self.l_name_box.add(self.change_name_entry)
            self.change_name_entry.show()
            self.change_name_confirm = gtk.Button("Make Change")
            self.change_name_confirm.connect("clicked", self.change_l_name_end)
            self.change_name_confirm.show()
            self.l_name_box.add(self.change_name_confirm)
            
    def change_l_name_end(self, widget):
        #Second half of processes required to change the client's first name in the client management window. (Sytactically required to be this way)
        l_name = self.change_name_entry.get_text()
        client_name = self.display_f_name.get_text()+" "+l_name
        old_client_name = self.display_f_name.get_text()+" "+self.old_l_name
        self.new_client(client_name, self.display_f_name.get_text(), l_name, clients[old_client_name].email)
        del clients[self.old_name]
        self.selector_box.remove(self.client_select)
        self.client_select = gtk.combo_box_new_text()
        self.selector_box.add(self.client_select)
        self.client_select.show()
        self.client_select.insert_text(0, client_name)
        model = self.client_select.get_model()
        index = self.client_select.get_active()
        self.selected_client = model[index][0]
        for entry in clients:
            if entry != client_name:
                self.client_select.append_text(clients[entry].name)
        for entry in appointments:
            if appointments[entry].my_client == old_client_name:
                year = appointments[entry].my_year
                month = appointments[entry].my_month
                day = appointments[entry].my_day
                time = appointments[entry].my_time
                del appointments[entry]
                new_appointment(year, month, day, time, 1, client_name)
        self.client_select.set_active(0)
        self.client_select.connect("changed", self.cb_changed)
        self.l_name_box.remove(self.change_name_entry)
        self.l_name_box.remove(self.change_name_confirm)
        self.display_l_name = gtk.Label(l_name)
        self.l_name_box.add(self.display_l_name)
        self.display_l_name.show()
        self.change_l_name = gtk.Button(label="Change Last Name")
        self.change_l_name.connect("clicked", self.change_l_name_begin)
        self.l_name_box.add(self.change_l_name)
        self.change_l_name.show()
        self.selector_box.remove(self.client_select)
        self.client_select = gtk.combo_box_new_text()
        self.selector_box.add(self.client_select)
        self.client_select.append_text(client_name)
        for entry in clients:
            if entry != client_name:
                self.client_select.append_text(clients[entry].name)
        self.client_select.set_active(0)
        self.client_select.connect("changed", self.cb_changed)
        self.client_select.show()
        self.days_info()

    def change_f_name_begin(self, widget):
        self.old_f_name=self.display_f_name.get_text()
        self.old_name = self.old_f_name+" "+self.display_l_name.get_text()
        self.selector_box.remove(self.client_select)
        self.client_select = gtk.combo_box_new_text()
        self.selector_box.add(self.client_select)
        self.client_select.append_text(self.old_name)
        self.client_select.connect("changed", self.dummy)
        f_name = self.display_f_name.get_text()
        if f_name not in ("", " "):
            self.f_name_box.remove(self.display_f_name)
            self.f_name_box.remove(self.change_f_name)
            del self.display_f_name
            del self.change_f_name
            self.change_name_entry = gtk.Entry(max=0)
            self.change_name_entry.set_text(f_name)
            self.f_name_box.add(self.change_name_entry)
            self.change_name_entry.show()
            self.change_name_confirm = gtk.Button("Make Change")
            self.change_name_confirm.connect("clicked", self.change_f_name_end)
            self.change_name_confirm.show()
            self.f_name_box.add(self.change_name_confirm)
        
    def change_f_name_end(self, widget):
        f_name = self.change_name_entry.get_text()
        client_name = f_name+" "+self.display_l_name.get_text()
        old_client_name = self.old_f_name+" "+self.display_l_name.get_text()
        self.new_client(client_name, f_name, self.display_l_name.get_text(), clients[old_client_name].email)
        del clients[self.old_name]
        self.selector_box.remove(self.client_select)
        self.client_select = gtk.combo_box_new_text()
        self.selector_box.add(self.client_select)
        self.client_select.show()
        self.client_select.insert_text(0, client_name)
        model = self.client_select.get_model()
        index = self.client_select.get_active()
        self.selected_client = model[index][0]
        for entry in clients:
            if entry != client_name:
                self.client_select.append_text(clients[entry].name)
        for entry in appointments:
            if appointments[entry].my_client == old_client_name:
                year = appointments[entry].my_year
                month = appointments[entry].my_month
                day = appointments[entry].my_day
                time = appointments[entry].my_time
                del appointments[entry]
                new_appointment(year, month, day, time, 1, client_name)
        self.client_select.set_active(0)
        self.client_select.connect("changed", self.cb_changed)
        self.f_name_box.remove(self.change_name_entry)
        self.f_name_box.remove(self.change_name_confirm)
        self.display_f_name = gtk.Label(f_name)
        self.f_name_box.add(self.display_f_name)
        self.display_f_name.show()
        self.change_f_name = gtk.Button(label="Change First Name")
        self.change_f_name.connect("clicked", self.change_f_name_begin)
        self.f_name_box.add(self.change_f_name)
        self.change_f_name.show()
        self.selector_box.remove(self.client_select)
        self.client_select = gtk.combo_box_new_text()
        self.selector_box.add(self.client_select)
        self.client_select.append_text(client_name)
        for entry in clients:
            if entry != client_name:
                self.client_select.append_text(clients[entry].name)
        self.client_select.set_active(0)
        self.client_select.connect("changed", self.cb_changed)
        self.client_select.show()
        self.days_info()
        # #########################################################

    def change_email_begin(self, widget):
        self.selector_box.remove(self.client_select)
        self.old_email = self.display_e_mail.get_text()
        self.change_f_name.connect("clicked", self.dummy)
        self.change_l_name.connect("clicked", self.dummy)
        self.email_box.remove(self.display_e_mail)
        self.email_box.remove(self.change_email)
        self.new_email = gtk.Entry(max=0)
        self.email_box.add(self.new_email)
        self.new_email.set_text(self.old_email)
        self.new_email.show()
        self.new_email_confirm = gtk.Button("Make Changes")
        self.new_email_confirm.show()
        self.email_box.add(self.new_email_confirm)
        self.new_email_confirm.connect("clicked", self. change_email_second)
        
    def change_email_second(self, widget):
        new_email = self.new_email.get_text()
        client_name = self.display_f_name.get_text()+" "+self.display_l_name.get_text()
        clients[client_name].email = new_email
        self.email_box.remove(self.new_email)
        self.email_box.remove(self.new_email_confirm)
        self.display_e_mail = gtk.Label(clients[client_name].email)
        self.display_e_mail.show()
        self.email_box.add(self.display_e_mail)
        self.change_email = gtk.Button(label="Change Email Address")
        self.change_email.connect("clicked", self.change_email_begin)
        self.change_email.show()
        self.email_box.add(self.change_email)
        self.client_select = gtk.combo_box_new_text()
        self.selector_box.add(self.client_select)
        self.client_select.insert_text(0, client_name)
        for entry in clients:
            if clients[entry].name != client_name:
                self.client_select.append_text(clients[entry].name)
        self.client_select.set_active(0)
        self.client_select.show()
        self.client_select.connect("changed", self.cb_changed)
        self.change_f_name.connect("clicked", self.change_f_name_begin)
        self.change_l_name.connect("clicked", self.change_l_name_begin)
    def kill_program(self, window):
        save_data(self)
        gtk.main_quit()

    def __init__(self):
        
        #Set the main settings and variables.
        self.window = None
        self.font = None
        self.font_dialog = None
        self.flag_checkboxes = 5*[None]
        self.settings = 5*[0]
        self.marked_date = 31*[0]
        
        #Set up the high-level window for use.
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Scheduler')
        window.set_border_width(5)
        window.connect("destroy", self.kill_program)
        window.set_resizable(False)
        
        #Create a high-level container
        high_level = gtk.VBox(False, self.DEF_PAD_SMALL)
        window.add(high_level)
        
        #Add menus and items
        file_menu = gtk.Menu()
        save_item = gtk.MenuItem("Save")
        save_item.connect_object("activate", save_data, "file.save")
        
        help_menu = gtk.Menu()
        about_item = gtk.MenuItem("Help")
        about_item.connect_object("activate", self.about_popup, "about_menu")
        
        help_menu.append(about_item)
        about_item.show()

        file_menu.append(save_item)
        save_item.show()
        
        #Add menu bar
        menu_bar = gtk.MenuBar()
        high_level.add(menu_bar)
        menu_bar.show()
        
        file_item = gtk.MenuItem("File")
        file_item.show()
        file_item.set_submenu(file_menu)
        menu_bar.append(file_item)
        
        help_item = gtk.MenuItem("Help")
        help_item.show()
        help_item.set_submenu(help_menu)
        menu_bar.append(help_item)
        
        #Create a container for our objects 
        main_container = gtk.HBox(False, self.DEF_PAD)
        high_level.add(main_container)
        
        #Set up the box to contain our to-be-created calendar widget.
        calendar_box = gtk.VBox()
        main_container.add(calendar_box)
        
        #Create the calendar widget, and add it to our previously created container.
        calendar_frame = gtk.Frame("Calendar")
        calendar_box.pack_start(calendar_frame, False, True, self.DEF_PAD)
        calendar = gtk.Calendar()
        self.window = calendar
        calendar_frame.add(calendar)
        calendar.connect("month_changed", self.calendar_month_changed)
        calendar.connect("day_selected", self.calendar_day_selected)
        calendar.connect("prev_month", self.calendar_prev_month)
        calendar.connect("next_month", self.calendar_next_month)
        calendar.connect("prev_year", self.calendar_prev_year)
        calendar.connect("next_year", self.calendar_next_year)
        
        #Add notebook for settings and client management
        multi_box = gtk.Notebook()
        calendar_box.add(multi_box)
        multi_box.set_tab_pos(gtk.POS_TOP)
        multi_box.set_size_request(200, 250)
        
        #Add client creation window
        add_clients = gtk.Frame("Add clients to your database")
        vbox = gtk.VBox(False, 0)
        add_clients.add(vbox)
        vbox.show()
        
        self.first_name = gtk.Frame("First name")
        vbox.add(self.first_name)
        self.f_name = gtk.Entry(max=0)
        self.first_name.add(self.f_name)
        
        last_name = gtk.Frame("Last name")
        vbox.add(last_name)
        self.l_name = gtk.Entry(max=0)
        last_name.add(self.l_name)
        
        email_addy = gtk.Frame("Email address")
        vbox.add(email_addy)
        self.e_mail = gtk.Entry(max=0)
        email_addy.add(self.e_mail)
        add_client_label = gtk.Label("Add Client")
        multi_box.append_page(add_clients, add_client_label)
        make_client = gtk.Button(label="Make New Client")
        vbox.add(make_client)
        make_client.connect("clicked", self.make_new_client)#Connect to function
        
        #Add client management window
        manage_clients = gtk.Frame("Manage Existing Clients")
        vbox = gtk.VBox(False, 0)
        manage_clients.add(vbox)
        vbox.show()
        
        selector_frame = gtk.Frame("")
        vbox.add(selector_frame)
        self.selector_box = gtk.VBox(False, 0)
        selector_frame.add(self.selector_box)
        self.client_select = gtk.combo_box_new_text()
        self.selector_box.add(self.client_select)
        for entry in clients:
            self.client_select.append_text(clients[entry].name)
        self.client_select.connect("changed", self.cb_changed)
        
        self.display_first_name = gtk.Frame("First name")
        vbox.add(self.display_first_name)
        self.f_name_box = gtk.VBox(False, 0)
        self.display_first_name.add(self.f_name_box)
        self.display_f_name = gtk.Label("")
        self.f_name_box.add(self.display_f_name)
        self.change_f_name = gtk.Button(label="Change First Name")
        self.change_f_name.connect("clicked", self.change_f_name_begin)
        self.f_name_box.add(self.change_f_name)
        
        self.display_last_name = gtk.Frame("Last name")
        vbox.add(self.display_last_name)
        self.l_name_box = gtk.VBox(False, 0)
        self.display_l_name = gtk.Label("")
        self.display_last_name.add(self.l_name_box)
        self.l_name_box.add(self.display_l_name)
        self.change_l_name = gtk.Button(label="Change Last Name")
        self.change_l_name.connect("clicked", self.change_l_name_begin)
        self.l_name_box.add(self.change_l_name)
        
        self.display_email_addy = gtk.Frame("Email address")
        vbox.add(self.display_email_addy)
        self.email_box = gtk.VBox(False, 0)
        self.display_e_mail = gtk.Label("")
        self.display_email_addy.add(self.email_box)
        self.email_box.add(self.display_e_mail)
        self.change_email = gtk.Button(label="Change Email Address")
        self.change_email.connect("clicked", self.change_email_begin)
        self.email_box.add(self.change_email)
        
        self.del_client_frame = gtk.Frame()
        vbox.add(self.del_client_frame)
        del_client_box = gtk.VBox(False, 0)
        self.del_client_frame.add(del_client_box)
        self.del_client = gtk.Button(label="Remove client")
        self.del_client.connect("clicked", self.remove_client)
        del_client_box.add(self.del_client)
        
        manage_client_label = gtk.Label("Manage Clients")
        multi_box.append_page(manage_clients, manage_client_label)
        
        #Add A Scrolled Window
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_border_width(5)
        scrolled_window.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_ALWAYS)
        main_container.add(scrolled_window)
        scrolled_window.show()
        
        #Add a container for our scrolled window's child widgets
        self.scrolled_container = gtk.HBox(False, self.DEF_PAD)
        scrolled_window.add_with_viewport(self.scrolled_container)
        scrolled_window.set_size_request(900, 500)
        
        self.cal_day = 0
        self.cal_month = 0
        self.cal_year = 0
        
        #Monday
        self.monday_frame = gtk.Frame("No date selected")
        self.scrolled_container.add(self.monday_frame)
        self.monday_display_day = gtk.VBox(False, self.DEF_PAD)
        self.monday_frame.add(self.monday_display_day)
        
        for time in my_times:
            self.time_frame = gtk.Frame(time)
            self.monday_display_day.add(self.time_frame)
            callable_times[("Monday", time)] = time
            callable_times[("Monday", time)] = gtk.HBox(False, self.DEF_PAD_SMALL)
            callable_times[("Monday", time)].set_size_request(200, 25)
            self.time_frame.add(callable_times[("Monday", time)])
            try:
                time_label = gtk.Label(appointments[(self.monday_year, self.monday_month, self.monday_day, time)].my_client)
            except:
                time_label = gtk.Label("Kein appointmenten")
            callable_times[("Monday", time)].add(time_label)
            
        #Tuesday
        self.tuesday_frame = gtk.Frame("No date selected")
        self.scrolled_container.add(self.tuesday_frame)
        self.tuesday_display_day = gtk.VBox(False, self.DEF_PAD)
        self.tuesday_frame.add(self.tuesday_display_day)
        
        for time in my_times:
            self.time_frame = gtk.Frame(time)
            self.tuesday_display_day.add(self.time_frame)
            callable_times[("Tuesday", time)] = time
            callable_times[("Tuesday", time)] = gtk.HBox(False, self.DEF_PAD_SMALL)
            callable_times[("Tuesday", time)].set_size_request(200, 25)
            self.time_frame.add(callable_times[("Tuesday", time)])
            try:
                time_label = gtk.Label(appointments[(self.tuesday_year, self.tuesday_month, self.tuesday_day, time)].my_client)
            except:
                time_label = gtk.Label("")
            callable_times[("Tuesday", time)].add(time_label)
        
        #Wednesday
        self.wednesday_frame = gtk.Frame("No date selected")
        self. scrolled_container.add(self.wednesday_frame)
        self.wednesday_display_day = gtk.VBox(False, self.DEF_PAD)
        self.wednesday_frame.add(self.wednesday_display_day)
        
        for time in my_times:
            self.time_frame = gtk.Frame(time)
            self.wednesday_display_day.add(self.time_frame)
            callable_times[("Wednesday", time)] = time
            callable_times[("Wednesday", time)] = gtk.HBox(False, self.DEF_PAD_SMALL)
            callable_times[("Wednesday", time)].set_size_request(200, 25)
            self.time_frame.add(callable_times[("Wednesday", time)])
            try:
                time_label = gtk.Label(appointments[(self.wednesday_year, self.wednesday_month, self.wednesday_day, time)].my_client)
            except:
                time_label = gtk.Label("")
            callable_times[("Wednesday", time)].add(time_label)
        
        #Thursday
        self.thursday_frame = gtk.Frame("No date selected")
        self.scrolled_container.add(self.thursday_frame)
        self.thursday_display_day = gtk.VBox(False, self.DEF_PAD)
        self.thursday_frame.add(self.thursday_display_day)
        
        for time in my_times:
            self.time_frame = gtk.Frame(time)
            self.thursday_display_day.add(self.time_frame)
            callable_times[("Thursday", time)] = time
            callable_times[("Thursday", time)] = gtk.HBox(False, self.DEF_PAD_SMALL)
            callable_times[("Thursday", time)].set_size_request(200, 25)
            self.time_frame.add(callable_times[("Thursday", time)])
            try:
                time_label = gtk.Label(appointments[(self.thursday_year, self.thursday_month, self.thursday_day, time)].my_client)
            except:
                time_label = gtk.Label("")
            callable_times[("Thursday", time)].add(time_label)
        
        #Friday
        self.friday_frame = gtk.Frame("No date selected")
        self.scrolled_container.add(self.friday_frame)
        self.friday_display_day = gtk.VBox(False, self.DEF_PAD)
        self.friday_frame.add(self.friday_display_day)
        
        for time in my_times:
            self.time_frame = gtk.Frame(time)
            self.friday_display_day.add(self.time_frame)
            callable_times[("Friday", time)] = time
            callable_times[("Friday", time)] = gtk.HBox(False, self.DEF_PAD_SMALL)
            callable_times[("Friday", time)].set_size_request(200, 25)
            self.time_frame.add(callable_times[("Friday", time)])
            try:
                time_label = gtk.Label(appointments[(self.friday_year, self.friday_month, self.friday_day, time)].my_client)
            except:
                time_label = gtk.Label("")
            callable_times[("Friday", time)].add(time_label)
        
        #Saturday
        self.saturday_frame = gtk.Frame("No date selected")
        self.scrolled_container.add(self.saturday_frame)
        self.saturday_display_day = gtk.VBox(False, self.DEF_PAD)
        self.saturday_frame.add(self.saturday_display_day)
        
        for time in my_times:
            self.time_frame = gtk.Frame(time)
            self.saturday_display_day.add(self.time_frame)
            callable_times[("Saturday", time)] = time
            callable_times[("Saturday", time)] = gtk.HBox(False, self.DEF_PAD_SMALL)
            callable_times[("Saturday", time)].set_size_request(200, 25)
            self.time_frame.add(callable_times[("Saturday", time)])
            try:
                time_label = gtk.Label(appointments[(self.saturday_year, self.saturday_month, self.saturday_day, time)].my_client)
            except:
                time_label = gtk.Label("")
            callable_times[("Saturday", time)].add(time_label)
        
        #Sunday
        self.sunday_frame = gtk.Frame("No date selected")
        self.scrolled_container.add(self.sunday_frame)
        self.sunday_display_day = gtk.VBox(False, self.DEF_PAD)
        self.sunday_frame.add(self.sunday_display_day)
        
        for time in my_times:
            self.time_frame = gtk.Frame(time)
            self.sunday_display_day.add(self.time_frame)
            callable_times[("Sunday", time)] = time
            callable_times[("Sunday", time)] = gtk.HBox(False, self.DEF_PAD_SMALL)
            callable_times[("Sunday", time)].set_size_request(200, 25)
            self.time_frame.add(callable_times[("Sunday", time)])
            try:
                time_label = gtk.Label(appointments[(self.sunday_year, self.sunday_month, self.sunday_day, time)].my_client)
            except:
                time_label = gtk.Label("")
            callable_times[("Sunday", time)].add(time_label)
        calendar.select_day(1)
        window.show_all()
def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    print "#################################################"
    print "#    Your Friendly Nieghborhood Debug Window    #"
    print "#                      :D                       #"
    print "#          Copyright 2008 Daniel Ralston        #"
    print "#################################################"
    try:
        get_data()
    except:
        print "Fresh slate!"
    MainWindow()
    main()
