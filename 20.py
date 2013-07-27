import sys
import shelve
class User:
    def __init__(self, username, password, rootpriv, adminpri, passchgpriv):
        self.username = username
        self.password = password
        self.rootpriv = rootpriv
        self.adminpri = adminpri
        self.passchgpriv = passchgpriv
    def userinfo(self, user, go):
        print "Username:                  ",self.username
        print "Password:                  ",self.password
        print "Root:                      ",self.rootpriv
        print "Admin:                     ",self.adminpri
        print "Password Change Permission:",self.passchgpriv
        print ""
        if go == "root":
            root(user)
        else:
            main(user)
Daniel = User("Daniel", "Feathers", 1, 1, 1)
Oliver = User("Oliver", "Cat", 0, 0, 1)
users = {"Daniel": Daniel, "Oliver": Oliver}
#users = {}
nul = 0
badcommand = "Unrecognized command"
baduser = "That user does not exist."
yes = ("Y", "y", "Yes", "yes")
no = ("N", "n", "No", "no")
maincall = ("Menu", "menu", "Main", "main")
quitcall = ("Quit", "quit", "exit", "Exit")
logoutcall = ("logout", "logoff", "#logout", "#logoff")
#Define the login module
def saveusers():
    myShelveUsers = shelve.open('userlist')         #open a shelve
    for key in myShelveUsers:
        del myShelveUsers[key]
    for key in users:                     
        myShelveUsers[key] = users[key]             #and just treat it like a
    myShelveUsers.close()                           #normal dictionary!
def getuser(name):
    myShelveUsers = shelve.open('userlist')         #access the shelve like a 
    gotuser = myShelveUsers[name]                      #dictionary
    users[name] = gotuser
    myShelveUsers.close()
    return gotuser
def getusers():
    myShelveUsers = shelve.open('userlist')         #access the shelve like a 
    for key in myShelveUsers:
        gotuser = myShelveUsers[key]                      #dictionary
        users[key] = gotuser
    myShelveUsers.close()
def login():
    #Create login prompt and record the command issued by the user
    print "login>"
    user = str(raw_input())
    #If the value provided by the user exists in the library bring up the password prompt
    if user in users:
        print "password>"
        pas = str(raw_input())
        #If the password matches the password of the given user, go to the main menu
        if pas == users[user].password:
            main(user)
        #If not, reject the command
        else:
            print "Unrecognized password."
            login()
    #If the value given by the user is quit, stop the program
    elif user in quitcall:
        saveusers()
        sys.exit
    #If the value doesn't match either of these, reject the value and ask if the user would like to add a new login
    else:
        print baduser
        login()
#Define the main body of the program        
def main(user):
    print "Hello, ",user
    print "Type Dir for help."
    #Add a prompt
    print ""
    print "prompt>"
    prompt = str(raw_input())
    #Checks for various recognized commands
    if prompt[0] == "#":
        newprompt = prompt.strip("#")
        if newprompt == "passchange":
            if users[user].passchgpriv == 1:
                passchgbool(user, 0)
            else:
                print "You do not have sufficient privileges to change your password."
                main(user)
        elif newprompt == "password":
            print users[user].password
            main(user)
        elif newprompt == "info":
            users[user].userinfo(user, "main")
        elif newprompt in logoutcall:
            logout(user)
        else:
            print badcommand
            main(user)
    elif prompt in ("dir", "Dir", "Help", "help"):
        dir(user, 1)
    elif prompt == "about":
        print "This program was aimed to imitate a fully working operating system. \nThe project was started by Daniel Ralston, a tenth grade student, in November \n2007 as a way to teach himself the Python Programming Language."
        del prompt
        main(user)
    elif prompt == "root" and users[user].rootpriv == 1:
        root(user)
    elif prompt == "root" and users[user].rootpriv == 0:
        print "You do not have root access."
        main(user)
#    elif prompt == "admin" and users[user].adminpri == 1:
        pass#admin(user)
#    elif prompt == "admin" and users[user].adminpri != 1:
        print "You do not have admin privileges."
        main(user)
    elif prompt in quitcall:
        saveusers()
        sys.exit()
    else:
        print badcommand
        main(user)
#Self password change confirmation module.
def passchgbool(user, inroot):
    #Asks if the user really wants to change his password
    print "Do you want to change your password?[y/n]>"
    chgbool = str(raw_input())
    if chgbool in yes:
        #If yes, go to passchange
        passchange(user, inroot)
    elif chgbool in no:
        print "Your password has not been altered."
        #if not, go to main
        wherego(user, inroot)
    elif chgbool == "back":
        wherego(user, inroot)
    elif chgbool in maincall:
        main(user)
    else:
        print badcommand
        passchgbool(user)
def wherego(user, inroot):
    if inroot == 1:
        root(user)
    else:
        main(user)
        
#Self password change module.
def passchange(user, inroot):
    oldpass = str(raw_input("old_password>"))
    if oldpass == users[user].password:
        chgpass = str(raw_input("new_password>"))#Asks for new password
        chgpass2 = str(raw_input("confirm>"))#Confirms
        if chgpass == chgpass2:#Checks if they match
            del users[user].password#Deletes old password
            users[user].password = chgpass#Changes the password
            print "Your password has been changed."
            wherego(user, inroot)
        else:
            print "Your password has not been changed. \nThe confirmation password did not match the initial try."
            passchgbool(user, inroot)
    elif oldpass in ("back", "Back") and oldpass != users[user].password:
        wherego(user, inroot)
    elif oldpass in maincall: #If the user is trying to go back, go back.
        main(user)
    else:
        print "Your confirmation password does not match the password in memory."
        passchange(user)

#root main base.
def root(user):
    print "Warning, system damage can be done from root mode."
    print "Hello, ",user,", you are running root mode."
    print "While in root mode, typing in \'root\' will return you to the root menu, except in certain contexts."
    print "root>"
    rootfresh = str(raw_input())
    if rootfresh[0] == "#":
        newrootfresh = rootfresh.strip("#")
        if newrootfresh == "passchange":
            if users[user].passchgpriv == 1:
                passchgbool(user, 1)
            else:
                print "You do not have sufficient privileges to change your password."
                main(user)
        elif newrootfresh == "password":
            print users[user].password
            main(user)
        elif newrootfresh == "info":
            users[user].userinfo(user, "main")
        else:
            print badcommand
            main(user)
    elif rootfresh[0] == "$":
        rootothers(user, rootfresh)
    elif rootfresh == "%":
        rootsys(user)
    elif rootfresh == "dir":
        rootdir(user, 1)
    elif rootfresh == "root0":
        main(user)
    elif rootfresh == "main":
        main(user)
    elif rootfresh in quitcall:
        saveusers()
        sys.exit
    elif rootfresh == "root":
        print "You are already running in root mode."
        root(user)
    elif rootfresh == "#logout":
        logout(user)
    else:
        print badcommand
        root(user)
def rootsys(user):
    print "root%sysadmin>"
    rootsyscom = str(raw_input())
    if rootsyscom == "%password_index":
        for key in users:
            print key,":", users[key].password
    elif rootsyscom == "%deluser":
        rootdeluserbool(user)
    elif rootsyscom == "%newuser":
        rootnewuserbool(user)
    elif rootsyscom == "dir":
        rootdir(user, 1)
    elif rootsyscom == "root0":
        main(user)
    elif rootsyscom == "main":
        main(user)
    elif rootsyscom in quitcall:
        saveusers()
        sys.exit
    elif rootsyscom == "root":
        root(user)
    elif rootsyscom == "#logout":
        logout(user)
    elif rootsyscom == "back":
        root(user)
    else:
        print badcommand
        rootsys(user)
def rootnewuserbool(user):
    print "Do you want to create a new user? [y/n]>"
    yn = str(raw_input())
    if yn in yes:
        rootnewuser(user)
    elif yn in no:
        print "No user has been created."
        rootsys(user)
    else:
        print badcommand
        rootnewuserbool(user)
def rootnewuser(user):
    print "newusername>"
    newusername = str(raw_input())
    if newusername not in ("root", "Root", "back", "Back", maincall, users):
        print "new_password>"
        newpass = str(raw_input())
        print "confirm>"
        conf = str(raw_input())
        if newpass == conf:
            users[newusername] = newusername
            users[newusername] = User(newusername, newpass, 0, 0, 0)
            print "User", users[newusername].username, "has been added."
            rootsys(user)
        else:
            print "Password does not match the confirmation password."
            rootnewuser(user)
    elif newusername in ("root", "Root"):
        root(user)
    elif newusername in ("back", "Back"):
        rootsys(user)
    elif newusername in maincall:
        main(user)
    else:
        print "That username already has an entry in the database."
        rootnewuser(user)
def rootdeluserbool(user):
    print "Are you sure you want to delete a user?[y/n]>"
    yorn = str(raw_input())
    if yorn in yes:
        rootdeluser(user)
    elif yorn in no:
        print "No users have been altered."
        rootsys(user)
    else:
        print badcommand
        rootdeluserbool(user)
def rootdeluser(user):
    print "%target_user>"
    deltarget = str(raw_input())
    if deltarget not in (user, "Daniel") and deltarget in users:
        print "This action can't be reversed or recovered."
        print "Are you sure you want to delete", deltarget, "?[y/n]>"
        yorn = str(raw_input())
        if yorn in yes:
            deluser(user, deltarget)
        if yorn in no:
            print targetuser, "has not been altered."
            rootsys(user)
        else:
            print badcommand
    elif deltarget in (user, "Daniel"):
        print "You can't delete the active user, or the main root user."
        rootdeluser(user)
    elif deltarget == "back":
        rootsys(user)
    elif deltarget == "root":
        root(user)
    elif deltarget == "root0":
        main(user)
    elif deltarget == "main":
        main(user)
    else:
        print baduser
        rootdeluser(user)
def deluser(user, target):
    del users[target]
    print "User", target, "has been removed."
    rootsys(user)
def rootothers(user, rootfresh):
    targetuser = rootfresh.strip("$")
    if targetuser in users and targetuser != user:
        print "$", users[targetuser].username, "$prompt>"
        targetusercom = str(raw_input())
        if targetusercom == "$passchange":
            rootsetpass(user, targetuser)
        elif targetusercom == "$password":
            print users[targetuser].password
            main(user)
        elif targetusercom == "$info":
            users[targetuser].userinfo(user, "root")
        elif targetusercom == "switchuser":
            switchuser(user, rootfresh)
        elif targetusercom == "back":
            root(user)
        elif targetusercom in maincall:
            main(user)
        elif targetusercom in quitcall:
            saveusers()
            sys.exit
        else:
            print badcommand
            rootothers(user, rootfresh)
    elif targetuser == user:
        print "You must make changes to yourself from the main root menu."
        rootothers(user, rootfresh)
    else:
        print baduser
        root(user)
def switchuser(user, rootfresh):
    print "target_user>"
    rootfresh1 = str(raw_input())
    if rootfresh1 != user:
        rootothers(user, rootfresh1)
    else:
        print "You must make changes to yourself from the main root menu."
        rootothers(user, rootfresh)
def rootsetpass(user, targetuser):
    print "Do you want to change the password of",targetuser
    yn = str(raw_input())
    if yn in yes:
        print "newpass>"
        newpas = str(raw_input())
        print "confirm>"
        confirm = str(raw_input())
        if newpas == confirm:
            users[targetuser].password = newpas
            root(user)
        else:
            print "New password does not match confirmation password."
            rootsetpass(user, targetuser)
    elif yn in no:
        print "The password of", targetuser,"has not been altered."
        rootothers(user)
    else:
        print badcommand
        root(user)
def dir(user, isroot):
    print "  Directory of commands and modules"
    print "   Modules:  $(User commands), %(System commands)"
    print ""
    print "  Answers are y or n."
    print "  \'#\' refers to actions that affect the current user."
    print "   dir"
    print "   quit"
    print "   about"
    print "   main                  Return to the main menu."
    print "   back                  Return to the parent prompt if you are in a function."
    print "   #passchange           Changes your current password."
    print "   #password             Displays your current password."
    print "   #info                 Displays your user information."
    print "   #logout               Logs out."
    print ""
    if isroot == 1:
        print "   root                  Enters root mode if you have sufficient privileges."
        print "  The following commands only apply to root mode only."
        print "  To gain acces to the root prompt and if you have root privileges, type in \'root\' at the main prompt."
        print ""
        print "   root                  To return to the root menu at any point."
        print "   root0                 Deactivates root mode. Must be done from main root prompt."
        print "   main                  Same effect as root0"
        print "   back                  Returns you to the parent prompt if you are in a function."
        print ""
        print "   $username             Sets the prompt to make changes to"
        print "     $passchange         Resets the password"
        #print "     $setadmin          Entering a 1 or a 0 following this command gives admin privileges or removes them, respectively."
        #print "     $seeadmin          Displays the admin privileges for the target user."
        #print "     $rights            Press enter, and followed with the name of a program appended with a 0 or a 1 to give rights to use the program. (Currently inactive)"
        print "     $info               Displays the target user's info."
        print "     $deluser            Delete user."
        print "     $switchuser         For changing the target user while in \'$\'."
        print ""
        print "   %                     Higher level system and user commands."
        print "     %password_index     Lists each username and their passwords."
        print "     %newuser            Creates a new user."
        print "     %deluser            Same effect as $deluser"
        root(user)
    else:
        main(user)
def logout(user):
    print user,"has logged out."
    login()
getusers()
login()
"""saveusers()
del(Oliver)                                    #erase oliver
Oliver = getuser('Oliver')                     #let's see if we can get him back!
myin = str(raw_input(">"))
def prin(myinp):
    print users[myin].password
prin(myin)"""
