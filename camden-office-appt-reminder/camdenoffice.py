#!/usr/bin/env python

# ############################## #
#     (C)2008 Daniel Ralston     #
# Appointment Reminder Software  #
#           v0.2.0 alpha         #
#           callback.py          #
# ############################## #

import sys
import shelve
import pygtk
pygtk.require('2.0')
import gtk, pango
import time
import datetime
import calendar
import os

internal = True

#**Class Definitions**#
class Login:
    def __init__(self):
        self.window = None
        self.font = None
        self.font_dialog = None
        self.flag_checkboxes = 5*[None]
        self.settings = 5*[0]
        self.marked_date = 31*[0]
    
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Login')
        self.window.set_border_width(5)
        self.window.connect("destroy", self.kill)
        self.window.set_resizable(False)
        #self.window.set_size_request(200, 115)
        
        self.login_area = gtk.VBox(False, 10)
        self.window.add(self.login_area)
        if len(os.listdir((sys.path[0]+"/databases/"))) < 1:
            self.manage_users(widget = None, message = "Create new user", mode = "add")
            return
        
        self.select_user = gtk.combo_box_new_text()
        self.login_area.add(self.select_user)
        for i in os.listdir((sys.path[0]+"/databases/")):
            self.select_user.append_text(i)
        self.select_user.set_active(0)
                                
        buttons_box = gtk.HBox(False, 5)
        self.login_area.add(buttons_box)
        
        self.add_user = gtk.Button("Add User")
        buttons_box.add(self.add_user)
        
        self.manage = gtk.Button("Manage")
        self.manage.connect("clicked", self.manage_users)
        buttons_box.add(self.manage)
        
        buttons_box = gtk.HBox(False, 5)
        self.login_area.add(buttons_box)
        
        self.log_in_button = gtk.Button("Log In")
        self.log_in_button.connect("clicked", self.password)
        buttons_box.add(self.log_in_button)
        
        self.cancel_button = gtk.Button("Quit")
        self.cancel_button.connect("clicked", self.kill, True)
        buttons_box.add(self.cancel_button)
        
        self.window.show_all()
    def soft_init(self, widget = None):
        self.window.remove(self.login_area)
        
        self.login_area = gtk.VBox(False, 10)
        self.window.add(self.login_area)
        
        self.select_user = gtk.combo_box_new_text()
        self.login_area.add(self.select_user)
        for i in os.listdir((sys.path[0]+"/databases/")):
            self.select_user.append_text(i)
        self.select_user.set_active(0)
                                
        buttons_box = gtk.HBox(False, 5)
        self.login_area.add(buttons_box)
        
        self.add_user = gtk.Button("Add User")
        buttons_box.add(self.add_user)
        
        self.manage = gtk.Button("Manage")
        self.manage.connect("clicked", self.manage_users)
        buttons_box.add(self.manage)
        
        buttons_box = gtk.HBox(False, 5)
        self.login_area.add(buttons_box)
        
        self.log_in_button = gtk.Button("Log In")
        self.log_in_button.connect("clicked", self.password)
        buttons_box.add(self.log_in_button)
        
        self.cancel_button = gtk.Button("Quit")
        self.cancel_button.connect("clicked", self.kill, True)
        buttons_box.add(self.cancel_button)
        
        self.window.show_all()
    def log_in(self, user):
        database.current_user = user
        os.chdir((str(sys.path[0])+"/databases/"+user))
        self.kill()
    def kill(self, widget = None, kill_program = False):
        self.window.hide()
        self.window.hide_all()
        if kill_program == True:
            database.close_program = True
        gtk.main_quit()
    def manage_users(self, widget = None, message = "", mode = ""):
        self.window.remove(self.login_area)
        self.login_area = gtk.VBox(False, 5)
        self.window.add(self.login_area)
        if message != "":
            self.login_area.add(gtk.Label(message))
        if mode == "add":
            self.new_user = gtk.Entry(max = 32)
            self.login_area.add(self.new_user)
            
            add_button = gtk.Button("Add user")
            self.login_area.add(add_button)
            add_button.connect("clicked", self.add_user, True)
            cancel_button = gtk.Button("Cancel")
            self.login_area.add(cancel_button)
            cancel_button.connect("clicked", self.kill, True)
        else:
            self.users = gtk.combo_box_new_text()
            self.login_area.add(self.users)
            for i in os.listdir((sys.path[0]+"/databases/")):
                self.users.append_text(i)
            self.select_user.set_active(0)
            
            add_button = gtk.Button("Add user")
            add_button.connect("clicked", self.manage_users, "Add User", "add")
            self.login_area.add(add_button)
            
            remove_button = gtk.Button("Remove User")
            remove_button.connect("clicked", error_handler.error, "Remove User?", "yes/no", self.remove_user, self.soft_init, None, None, 320, 200, self.window)
            self.login_area.add(remove_button)
            
        self.window.show_all()
    def remove_user(self, widget = None, user = ""):
        model = self.users.get_model()
        index = self.users.get_active()
        user = model[index][0]
        try:
            os.remove(str(sys.path[0])+"/databases/"+user+"/"+"preferences")
            os.remove(str(sys.path[0])+"/databases/"+user+"/"+"key_base")
            os.remove(str(sys.path[0])+"/databases/"+user+"/"+"appointments")
            os.remove(str(sys.path[0])+"/databases/"+user+"/"+"clients")
        except:
            pass
        os.rmdir(str(sys.path[0])+"/databases/"+user)
        self.window.show_all()
        self.soft_init()
    def add_user(self, widget = None, prompt_pass = False):
        user = self.new_user.get_text()
        os.makedirs((str(sys.path[0])+"/databases/"+user), mode = 0774)
        self.window.show_all()
        if prompt_pass == True:
            self.password(True)
    def password(self, widget = None, new_pass = False, user = ""):
        if "preferences" not in os.listdir(sys.path[0]):
            new_pass = True
        if new_pass == False:
            model = self.select_user.get_model()
            index = self.select_user.get_active()
            user = model[index][0]
        self.window.remove(self.login_area)
        self.login_area = gtk.VBox(False, 5)
        self.window.add(self.login_area)
        if "preferences" in os.listdir(sys.path[0]) or new_pass == False:
            self.login_area.add(gtk.Label(("Password")))
        else:
            self.login_area.add(gtk.Label(("Enter New \nUniversal Password")))
        self.password_entry = gtk.Entry(max = 32)
        self.password_entry.set_visibility(False)
        self.login_area.add(self.password_entry)
        
        if "preferences" not in os.listdir(sys.path[0]) or new_pass == True:
            self.login_area.add(gtk.Label("Confirm Password:"))
            self.confirm_pass = gtk.Entry(max = 32)
            self.confirm_pass.set_visibility(False)
            self.login_area.add(self.confirm_pass)
        
        buttons_box = gtk.HBox(False, 5)
        self.login_area.add(buttons_box)
        
        log_in_button = gtk.Button("Log In")
        if "preferences" in os.listdir(sys.path[0]) or new_pass == False:
            log_in_button.connect("clicked", self.check_password, user)
        else:
            log_in_button.connect("clicked", self.new_password, user)
        buttons_box.add(log_in_button)
        
        cancel_button = gtk.Button("Cancel")
        if "preferences" in os.listdir(sys.path[0]) or new_pass == False:
            cancel_button.connect("clicked", self.soft_init)
        else:
            cancel_button.connect("clicked", self.kill, True)
        buttons_box.add(cancel_button)
        
        self.window.show_all()
        #self.log_in(user)
    def check_password(self, widget = None, user = None):
        if user != None:
            pass_check = self.password_entry.get_text()
            os.chdir((str(sys.path[0])))
            global_password = shelve.open("preferences")
            if pass_check == global_password["0"]:
                global_password.close()
                self.log_in(user)
            else:
                global_password.close()
                error_handler.error("Incorrect Password.", size_x = 128, size_y = 75)
                self.soft_init()
        else:
            global_password.close()
            self.soft_init()
    def new_password(self, widget = None, user = ""):
        new_pass = str(self.password_entry.get_text())
        if new_pass == self.confirm_pass.get_text():
            global_password = shelve.open("preferences")
            global_password["0"] = new_pass
            global_password.close()
            self.log_in(user)
        else:
            error_handler.error("Confirmation Password does\nnot match Password")
class Database:
#Provides a central storage unit to keep track of any and all our data
    def __init__(self):
        self.appointments = {}
        self.clients = {}
        self.preferences = {"save at close": True,
                            "send reminders": True, 
                            "send at login": True,
                            "company": "",
                            "email": "",
                            "email pass": ""}
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
        appts = self.appointments.copy()
        if name in self.clients:
            del self.clients[name]
            for entry in appts:
                if self.appointments[entry].client == name:
                    del self.appointments[entry]
        return
    def save_data(self, widget = None, user = "JRandomUser"):
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
    def get_data(self, widget = None, user = "JRandomUser"):
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

#**Main Program**#
class MainWindow:
    DEF_PAD_LARGE = 15
    DEF_PAD = 10
    DEF_PAD_SMALL = 5

    def draw_week_view(self):
        self.day_one_frame.remove(self.day_one)
        del self.day_one
        self.day_one = gtk.VBox(False, self.DEF_PAD_SMALL)
        self.day_one_frame.add(self.day_one)#The preceding resets the first day block for us

        self.day_two_frame.remove(self.day_two)
        del self.day_two
        self.day_two = gtk.VBox(False, self.DEF_PAD_SMALL)
        self.day_two_frame.add(self.day_two)
        
        self.day_three_frame.remove(self.day_three)
        del self.day_three
        self.day_three = gtk.VBox(False, self.DEF_PAD_SMALL)
        self.day_three_frame.add(self.day_three)
        
        self.day_four_frame.remove(self.day_four)
        del self.day_four
        self.day_four = gtk.VBox(False, self.DEF_PAD_SMALL)
        self.day_four_frame.add(self.day_four)
        
        year = self.calendar.get_date()[0]
        month = self.calendar.get_date()[1]+1
        day = self.calendar.get_date()[2]
        
        self.day_one_frame.set_label(database.day_names[datetime.date(year, month, day).weekday()+1]+", "+str(month)+", "+str(day)+", "+str(year))
        for i in range(1, 57):
            #Add the main timeslot
            date_and_time = year, month, day, i
            timeslot = gtk.Frame(database.possible_times[i])
            timeslot.set_size_request(100, 55)
            self.day_one.add(timeslot)
            timeslot.show()
            #print date_and_time
            if date_and_time in database.appointments:
                if str(type(database.appointments[date_and_time])) == "<type \'str\'>":
                    timeslot.add(gtk.Label(database.appointments[date_and_time]))
                else:
                    timeslot_selector = gtk.Button(database.appointments[date_and_time].client)
                    timeslot.add(timeslot_selector)
                    timeslot_selector.connect("clicked", self.select_timeslot, i, date_and_time)
            else:
                timeslot_selector = gtk.Button("")
                timeslot.add(timeslot_selector)
                timeslot_selector.connect("clicked", self.select_timeslot, i, date_and_time)
        day_2_date = Date(year, month, day).increment_days(1)
        year = day_2_date[0]
        month = day_2_date[1]
        day = day_2_date[2]
        self.day_two_frame.set_label(database.day_names[datetime.date(year, month, day).weekday()+1]+", "+str(month)+", "+str(day)+", "+str(year))
        del day_2_date
        for i in range(1, 57):
            #Add the main timeslot
            date_and_time = year, month, day, i
            timeslot = gtk.Frame(database.possible_times[i])
            timeslot.set_size_request(100, 55)
            self.day_two.add(timeslot)
            timeslot.show()
            #print date_and_time
            if date_and_time in database.appointments:
                if str(type(database.appointments[date_and_time])) == "<type \'str\'>":
                    timeslot.add(gtk.Label(database.appointments[date_and_time]))
                else:
                    timeslot_selector = gtk.Button(database.appointments[date_and_time].client)
                    timeslot.add(timeslot_selector)
                    timeslot_selector.connect("clicked", self.select_timeslot, i, date_and_time)
            else:
                timeslot_selector = gtk.Button("")
                timeslot.add(timeslot_selector)
                timeslot_selector.connect("clicked", self.select_timeslot, i, date_and_time)
        day_3_date = Date(year, month, day).increment_days(1)
        year = day_3_date[0]
        month = day_3_date[1]
        day = day_3_date[2]
        self.day_three_frame.set_label(database.day_names[datetime.date(year, month, day).weekday()+1]+", "+str(month)+", "+str(day)+", "+str(year))
        del day_3_date
        for i in range(1, 57):
            #Add the main timeslot
            date_and_time = year, month, day, i
            timeslot = gtk.Frame(database.possible_times[i])
            timeslot.set_size_request(100, 55)
            self.day_three.add(timeslot)
            timeslot.show()
            #print date_and_time
            if date_and_time in database.appointments:
                if str(type(database.appointments[date_and_time])) == "<type \'str\'>":
                    timeslot.add(gtk.Label(database.appointments[date_and_time]))
                else:
                    timeslot_selector = gtk.Button(database.appointments[date_and_time].client)
                    timeslot.add(timeslot_selector)
                    timeslot_selector.connect("clicked", self.select_timeslot, i, date_and_time)
            else:
                timeslot_selector = gtk.Button("")
                timeslot.add(timeslot_selector)
                timeslot_selector.connect("clicked", self.select_timeslot, i, date_and_time)
        day_4_date = Date(year, month, day).increment_days(1)
        year = day_4_date[0]
        month = day_4_date[1]
        day = day_4_date[2]
        self.day_four_frame.set_label(database.day_names[datetime.date(year, month, day).weekday()+1]+", "+str(month)+", "+str(day)+", "+str(year))
        del day_4_date
        for i in range(1, 57):
            #Add the main timeslot
            date_and_time = year, month, day, i
            timeslot = gtk.Frame(database.possible_times[i])
            timeslot.set_size_request(100, 55)
            self.day_four.add(timeslot)
            timeslot.show()
            #print date_and_time
            if date_and_time in database.appointments:
                if str(type(database.appointments[date_and_time])) == "<type \'str\'>":
                    timeslot.add(gtk.Label(database.appointments[date_and_time]))
                else:
                    timeslot_selector = gtk.Button(database.appointments[date_and_time].client)
                    timeslot.add(timeslot_selector)
                    timeslot_selector.connect("clicked", self.select_timeslot, "day1", i, date_and_time)
            else:
                timeslot_selector = gtk.Button("")
                timeslot.add(timeslot_selector)
                timeslot_selector.connect("clicked", self.select_timeslot, i, date_and_time)
                timeslot_selector.connect("clicked", self.select_timeslot, i, date_and_time)
        
        self.window.show_all()
    def select_timeslot(self, widget, time, date_and_time):
        #print self.right_hand_exists, "timeslot"
        self.control_frame.set_label(database.day_names[datetime.date(date_and_time[0], date_and_time[1], date_and_time[2]).weekday()+1]+", "+str(date_and_time[1]+1)+", "+str(date_and_time[2])+", "+str(date_and_time[0])+" "+str(database.possible_times[time]))
        self.draw_appointment_controller(date_and_time)
    def select_day(self, signal = None):
        self.draw_week_view()
        if self.right_hand_exists == True:
            self.control_container.remove(self.left_control)
            self.control_container.remove(self.right_control)
            self.main_control_container.remove(self.control_save_cancel_frame)
            self.control_frame.set_label("No Timeslot Selected")
            del self.date_and_time
        self.right_hand_exists = False
        #print self.right_hand_exists, "day"
        self.window.show_all()
    def save_timeslot_controller(self, widget, date_and_time):
        model = self.client_selector.get_model()
        index = self.client_selector.get_active()
        selected_client = model[index][0]
        if selected_client != "":
            length = self.length_spinner.get_value_as_int()/15
            
            email_bool = self.timeslot_email_bool.get_active()
            
            year = date_and_time[0]
            month = date_and_time[1]
            day = date_and_time[2]
            time = date_and_time[3]
            #if date_and_time in database.appointments:
            #    database.remove_appointment(year, month, day, time)        
            database.new_appointment(year, month, day, time, length, database.clients[selected_client].email, email_bool, selected_client, force = True)
        else:
            year = date_and_time[0]
            month = date_and_time[1]
            day = date_and_time[2]
            time = date_and_time[3]
            database.remove_appointment(year, month, day, time)
        
        self.select_day()
    def new_client_dialog(self, widget, name=""):
        #print self.right_hand_exists, "new client"
        self.window.hide_all()
        
        self.new_client_window = gtk.Window()
        self.new_client_window.set_title('Add Client')
        self.new_client_window.set_border_width(5)
        self.new_client_window.connect("destroy", self.destroy_new_client_dialog)
        self.new_client_window.set_resizable(False)
        
        #Add an object for eventual notes
        self.new_client_notes = []

        self.new_client = gtk.VBox(False, self.DEF_PAD)
        self.new_client_window.add(self.new_client)        
        
        self.name_frame = gtk.Frame("Name")
        self.name_box = gtk.Entry(max=32)
        self.new_client.add(self.name_frame)
        self.name_frame.add(self.name_box)
        
        self.email_frame = gtk.Frame("Email Address")
        self.email_box = gtk.Entry(max=32)
        self.new_client.add(self.email_frame)
        self.email_frame.add(self.email_box)
        
        self.new_client_email_bool = gtk.CheckButton(label = "Send Email Reminders")
        self.new_client_email_bool.set_active(database.preferences["send reminders"])
        self.new_client.add(self.new_client_email_bool)
        
        self.confirm_new_client = gtk.Button("Confirm New Client")
        self.confirm_new_client.connect("clicked", self.confirmed_new_client)
        self.new_client.add(self.confirm_new_client)
        
        self.discard_new_client = gtk.Button("Cancel")
        self.discard_new_client.connect("clicked", self.destroy_new_client_dialog)
        self.new_client.add(self.discard_new_client)
        
        self.new_client_window.show_all()
    def confirmed_new_client(self, widget):
        #print self.right_hand_exists, "confirmed"
        name = self.name_box.get_text()
        if name not in database.clients:
            email = self.email_box.get_text()
            email_bool = self.new_client_email_bool.get_active()
            
            database.new_client(name, email, email_bool)
            self.destroy_new_client_dialog()
            self.update_view()
        else:
            error_handler.error("Client of that name already exists in database.")
    def destroy_new_client_dialog(self, widget = None):
        #print self.right_hand_exists, "destroy new client"
        self.window.show_all()
        self.new_client_window.destroy()
    def update_view(self):
        #print self.right_hand_exists, "update"
        if self.right_hand_exists == True:
            self.draw_appointment_controller(self.date_and_time)
        self.draw_week_view()
    def auto_set_email_bool(self, widget, date_and_time):
        model = self.client_selector.get_model()
        index = self.client_selector.get_active()
        if model[index][0] != "":
            if date_and_time in database.appointments:
                self.timeslot_email_bool.set_active(database.appointments[date_and_time].email_bool)
            else:
                self.timeslot_email_bool.set_active(database.clients[model[index][0]].email_bool)  
        else:
            self.timeslot_email_bool.set_active(database.preferences["send reminders"])
    def draw_appointment_controller(self, date_and_time):
        #print self.right_hand_exists, "draw appt"
        #del self.left_control
        if self.right_hand_exists == True:
            self.control_container.remove(self.left_control)
            self.control_container.remove(self.right_control)
            
            self.main_control_container.remove(self.control_save_cancel_frame)
            self.control_save_cancel.remove(self.save_timeslot_changes)
            self.control_save_cancel.remove(self.cancel_timeslot_changes)
        #Add them anew
        self.left_control = gtk.VBox(False, self.DEF_PAD_LARGE)
        self.control_container.add(self.left_control)
            
        self.client_frame = gtk.Frame("Client")
        self.left_control.add(self.client_frame)
        self.client_container = gtk.HBox(False, self.DEF_PAD)
        self.client_frame.add(self.client_container)
        self.client_selector = gtk.combo_box_new_text()
        self.client_container.add(self.client_selector)
        if date_and_time in database.appointments:
            self.client_selector.insert_text(0, database.appointments[date_and_time].client)
        else:
            self.client_selector.insert_text(0, "")
        for entry in database.clients:
            if date_and_time in database.appointments:
                if entry != database.appointments[date_and_time].client:
                    self.client_selector.append_text(database.clients[entry].name)
            else:
                self.client_selector.append_text(database.clients[entry].name)
        if date_and_time in database.appointments:
            self.client_selector.append_text("")
        self.client_selector.set_size_request(250, 45)
        self.client_selector.set_active(0)
        self.timeslot_email_bool = gtk.CheckButton(label = "Send Email Reminders")
        self.left_control.add(self.timeslot_email_bool)
        self.client_selector.connect("changed", self.auto_set_email_bool, date_and_time)
        if date_and_time in database.appointments:
            self.timeslot_email_bool.set_active(database.appointments[date_and_time].email_bool)
        else:
            self.timeslot_email_bool.set_active(database.preferences["send reminders"])
        
        #This section simply adds a SpinButton to determine the length
        #(I decided to use a label to pad the right-hand side of the spinner)
        self.length_container = gtk.HBox(False, self.DEF_PAD)
        temp_adjustment = gtk.Adjustment(15, 15, 150, 15, 15, 0)
        self.length_spinner = gtk.SpinButton(adjustment = temp_adjustment, climb_rate = 0.1, digits = 0)
        self.length_spinner.set_numeric(True)
        self.length_spinner.set_snap_to_ticks(True)
        if date_and_time in database.appointments:
            self.length_spinner.set_value((database.appointments[date_and_time].length * 15))
        self.left_control.add(self.length_container)
        length_label = gtk.Label("Length in minutes:")
        blank = gtk.Label(("                    "*5))
        self.length_container.add(length_label)
        self.length_container.add(self.length_spinner)
        self.length_container.add(blank)
        
        self.right_control = gtk.VBox(False, 0)
        self.control_container.add(self.right_control)
        
        #Add the bottom save changes and cancel space
        self.control_save_cancel_frame = gtk.Frame()
        self.main_control_container.add(self.control_save_cancel_frame)
        self.control_save_cancel = gtk.HBox(False, 0)
        self.control_save_cancel_frame.add(self.control_save_cancel)
        
        #Add the bottom save changes and cancel buttons
        self.save_timeslot_changes = gtk.Button("Keep Changes")
        self.control_save_cancel.add(self.save_timeslot_changes)
        self.save_timeslot_changes.connect("clicked", self.save_timeslot_controller, date_and_time)
        self.cancel_timeslot_changes = gtk.Button("Discard Changes")
        self.cancel_timeslot_changes.connect("clicked", self.select_day)
        self.control_save_cancel.add(self.cancel_timeslot_changes)
        
        self.date_and_time = date_and_time
        
        self.right_hand_exists = True
        
        self.draw_week_view()
        
        self.window.show_all()
    def kill_program(self, widget = None):
        if database.preferences["save at close"] == True:
            database.save_data()
        gtk.main_quit()
        return 0
    def change_client_info(self, widget = None):
        model = self.manager_selector.get_model()
        index = self.manager_selector.get_active()
        selected_client = model[index][0]
        if model[index][0] not in (None, "" " "):
            self.manage_window.destroy()
            self.window.hide_all()
            
            self.change_window = gtk.Window()
            self.change_window.set_title(('Change '+selected_client+' Info'))
            self.change_window.set_border_width(5)
            self.change_window.connect("destroy", self.destroy_client_manager)
            self.change_window.set_resizable(False)
            
            change_frame = gtk.Frame()
            self.change_window.add(change_frame)
            
            change_container = gtk.VBox(False, 5)
            change_frame.add(change_container)
            
            self.name_entry = gtk.Entry(max = 32)
            change_container.add(self.name_entry)
            self.name_entry.set_text(selected_client)
            
            self.email_entry = gtk.Entry(max = 32)
            change_container.add(self.email_entry)
            self.email_entry.set_text(database.clients[selected_client].email)
            
            self.email_bool_box = gtk.CheckButton(label = "Send Email Reminders")
            change_container.add(self.email_bool_box)
            self.email_bool_box.set_active(database.clients[selected_client].email_bool)
            
            save_client_changes = gtk.Button("Save Changes")
            save_client_changes.connect("clicked", self.save_client_change)
            change_container.add(save_client_changes)
            
            discard_client_changes = gtk.Button("Cancel")
            change_container.add(discard_client_changes)
            discard_client_changes.connect("clicked", self.destroy_client_change)
            
            self.change_window.show_all()
        else:
            error_handler.error(None, "No Client Selected")
    def save_client_change(self, widget = None):
        self.window.hide_all()
        name = self.name_entry.get_text()
        email = self.email_entry.get_text()
        email_bool = self.email_bool_box.get_active()
        database.new_client(name, email, email_bool, None, True)
        self.destroy_client_change()
    def destroy_client_change(self, widget = None):
        self.change_window.destroy()
        self.window.hide_all()
        self.manage_clients()
    def manage_clients(self, widget = None, rem_container = None):
        self.window.hide_all()
        
        self.manage_window = gtk.Window()
        self.manage_window.set_title('Manage Clients')
        self.manage_window.set_border_width(5)
        self.manage_window.connect("destroy", self.destroy_client_manager)
        self.manage_window.set_resizable(False)
        
        self.manager_container = gtk.VBox(False, 10)
        self.manage_window.add(self.manager_container)
        
        self.manager_selector = gtk.combo_box_new_text()
        self.manager_container.add(self.manager_selector)
        for client in database.clients:
            self.manager_selector.append_text(client)
        self.manager_selector.set_active(0)
        
        alter_client = gtk.Button("Change Client Info")
        alter_client.connect("clicked", self.change_client_info)
        self.manager_container.add(alter_client)
        
        remove_client = gtk.Button("Remove Client")
        remove_client.connect("clicked", self.remove_selected_client)
        self.manager_container.add(remove_client)
        
        close_button = gtk.Button("Close")
        close_button.connect("clicked", self.destroy_client_manager)
        self.manager_container.add(close_button)
        
        self.manage_window.show_all()
    def remove_selected_client(self, widget = None):
        model = self.manager_selector.get_model()
        index = self.manager_selector.get_active()
        selected_client = model[index][0]
        if selected_client not in (None, "", " "):
            database.remove_client(None, selected_client)
            self.destroy_client_manager()
            self.manage_clients()
    def destroy_client_manager(self, widget = None):
        self.manage_window.destroy()
        self.window.show_all()
    def __init__(self):
        self.right_hand_exists = False
        
        #Set the main settings and variables.
        self.window = None
        self.font = None
        self.font_dialog = None
        self.flag_checkboxes = 5*[None]
        self.settings = 5*[0]
        self.marked_date = 31*[0]
        
        #Set up the high level window for use
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(("Camden Office Scheduler - "+database.current_user))
        self.window.set_border_width(5)
        self.window.connect("destroy", self.kill_program)
        self.window.set_resizable(False)
        self.window.set_size_request(1000, 670)
        
        #Create a hight-level container to work with.
        app_window = gtk.VBox(False, self.DEF_PAD_SMALL)
        self.window.add(app_window)
        
        #Add a container for menu bar
        menu_container = gtk.HBox(False, 0)
        app_window.add(menu_container)
        
        #Add menus and items
        file_menu = gtk.Menu()
        save_item = gtk.MenuItem("Save")
        save_item.connect_object("activate", database.save_data, "file.save")
        send_item = gtk.MenuItem("Send Reminders")
        #send_item.connect_object("activate", self.send reminders, "file.send", "jawohl")
        options_item = gtk.MenuItem("Options")
        #options_item.connect_object("activate", self.option_box, "options")
        
        file_menu.append(save_item)
        save_item.show()
        file_menu.append(send_item)
        send_item.show()
        file_menu.append(options_item)
        options_item.show()
        
        management_menu = gtk.Menu()
        add_client_item = gtk.MenuItem("Add Client")
        management_menu.append(add_client_item)
        add_client_item.connect("activate", self.new_client_dialog)
        
        manage_client_item = gtk.MenuItem("Manage Clients")
        management_menu.append(manage_client_item)
        manage_client_item.connect("activate", self.manage_clients)
        
        help_menu = gtk.Menu()
        about_item = gtk.MenuItem("Help")
        #about_item.connect_object("activate", self.about_popup, "about_menu")
        help_menu.append(about_item)
        about_item.show()
        
        #Add menu bar
        menu_bar = gtk.MenuBar()
        menu_bar.set_size_request(640, 20)
        menu_container.add(menu_bar)
        menu_bar.show()
        
        file_item = gtk.MenuItem("File")
        file_item.show()
        file_item.set_submenu(file_menu)
        menu_bar.append(file_item)
        
        management_item = gtk.MenuItem("Clients")
        management_item.set_submenu(management_menu)
        menu_bar.append(management_item)
        
        help_item = gtk.MenuItem("Help")
        help_item.show()
        help_item.set_submenu(help_menu)
        menu_bar.append(help_item)
        
        #Create the main container for the application
        self.main_app = gtk.Notebook()
        self.main_app.set_tab_pos(gtk.POS_LEFT)
        self.main_app.set_size_request(680, 380)
        app_window.add(self.main_app)    
        
        #Add the week view calendar
        self.week_view_window = gtk.ScrolledWindow()
        self.week_view_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        week_view_label = gtk.Label("Week View")
        self.main_app.append_page(self.week_view_window, week_view_label)
        self.week_view = gtk.HBox("False", 0)
        self.week_view_window.add_with_viewport(self.week_view)
        
        #Add the lower half of the application window
        self.lower_app = gtk.HBox(False, self.DEF_PAD)
        app_window.add(self.lower_app)
        
        #Create the calendar
        self.calendar_frame = gtk.Frame("Calendar")
        self.lower_app.add(self.calendar_frame)
        self.calendar = gtk.Calendar()
        self.calendar_frame.add(self.calendar)
        self.calendar.connect("day_selected", self.select_day)
        
        #Create the containers for individual days
        self.day_one_frame = gtk.Frame()
        self.week_view.add(self.day_one_frame)
        self.day_one = gtk.VBox(False, self.DEF_PAD)
        self.day_one_frame.add(self.day_one)
        
        self.day_two_frame = gtk.Frame()
        self.week_view.add(self.day_two_frame)
        self.day_two = gtk.VBox(False, self.DEF_PAD)
        self.day_two_frame.add(self.day_two)
        
        self.day_three_frame = gtk.Frame()
        self.week_view.add(self.day_three_frame)
        self.day_three = gtk.VBox(False, self.DEF_PAD)
        self.day_three_frame.add(self.day_three)
        
        self.day_four_frame = gtk.Frame()
        self.week_view.add(self.day_four_frame)
        self.day_four = gtk.VBox(False, self.DEF_PAD)
        self.day_four_frame.add(self.day_four)
        
        #Create the right-hand-side panel
        self.control_frame = gtk.Frame("No Timeslot Selected")
        self.lower_app.add(self.control_frame)
        self.main_control_container = gtk.VBox(False, 0)
        self.control_frame.add(self.main_control_container)
        self.control_container = gtk.HBox(False, self.DEF_PAD_LARGE)
        self.control_container.set_size_request(475, 100)
        self.main_control_container.add(self.control_container)
        
        #self.left_control = gtk.VBox(False, self.DEF_PAD_LARGE)
        #self.control_container.add(self.left_control)
        #self.right_control = gtk.VBox(False, 0)
        #self.control_container.add(self.right_control)

        self.draw_week_view()
        
        self.window.show_all()
if __name__ == "__main__":
    error_handler = Error_Handler()
    database = Database()
    if "databases" not in os.listdir(sys.path[0]):
        os.makedirs((str(sys.path[0])+"/databases/"), mode = 0774)
    print "Camden Office v 0.2.0a"
    #Login()
    #gtk.main()
    if internal == True:
        try:
            os.makedirs((str(sys.path[0])+"/databases/"+"JRandomUser"), mode = 0774)
        except:
            pass
        database.current_user = "JRandomUser"
        os.chdir((str(sys.path[0])+"/databases/"+"JRandomUser"))        
    if database.close_program == True:
        pass
    else:
        database.get_data()
        print database.clients, "\n\n"
        print database.appointments
        MainWindow()
        gtk.main()
