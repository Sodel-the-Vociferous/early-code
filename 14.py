import sys
copy = ["Daniel", "Oliver"]
passw = {"Daniel": "Feathers", "Oliver": "Cat"}
adminpri = {"Daniel": 1, "Oliver": 0}
adminext = {"Daniel": 1, "Oliver":0}
passchgpriv = {"Daniel": 1, "Oliver": 0}
nul = 0
rootpriv = {"Daniel": 1, "Oliver": 0}
badcommand = "Unrecognized command"
#user = "Daniel" comment this line out for the program to work correctly.
yes = ("Y", "y", "Yes", "yes")
no = ("N", "n", "No", "no")
maincall = ("Menu", "menu", "Main", "main")

#Define the login module
def login():
    #Create login prompt and record the command issued by the user
    user = str(raw_input("login>"))#
    #If the value provided by the user exists in the library bring up the password prompt
    if copy.count(user) > nul:
        pas = str(raw_input("password>"))
        #If the password matches the password of the given user, go to the main menu
        if pas == passw[user]:
            main(user)
        #If not, reject the command
        else:
            print "Unrecognized password."
            login()
    #If the value given by the user is quit, stop the program
    elif user in ("quit", "Quit"):
        sys.exit
    #If the value doesn't match either of these, reject the value and ask if the user would like to add a new login
    else:
        print "Username not recognized. "
        login()
#Define the main body of the program
def main(user):
    print "Hello, ",user
    print "Type Dir for help."
    #Add a prompt
    prompt = str(raw_input("prompt>"))
    #Checks for various recognized commands
    if prompt in ("dir", "Dir", "Help", "help"):
        dir(user)
    elif prompt == "about":
        print "This program was aimed to imitate a fully working operating system. \nThe project was started by Daniel Ralston, a tenth grade student, in November \n2007 as a way to teach himself the Python Programming Language."
        del prompt
        main(user)
    elif prompt == "#passchange":
        if passchgpriv[user] == 1:
            passchgbool(user)
        else:
            print "You do not have sufficient privileges to change your password."
            main(user)
    elif prompt == "logout":
        logout(user)
    elif prompt == "root" and rootpriv[user] == 1:
        root(user)
    else:
        print badcommand
        main(user)

def passchgbool(user):
    #Asks if the user really wants to change his password
    print "Do you want to change your password?>"
    chgbool = str(raw_input())
    if chgbool in yes:
        #If yes, go to passchange
        passchange(user)
    elif chgbool in no:
        #if not, go to main
        del prompt
        main(user)
    elif chgbool == "back":
        main(user)
    else:
        print badcommand
        
def passchange(user):
    chgpass = str(raw_input("new_password>"))#Asks for new password
    chgpass2 = str(raw_input("confirm>"))#Confirms
    if chgpass != "back" and chgpass2 != "back" and chgpass2 not in maincall and chgpass not in maincall:
        if chgpass == chgpass2:#Checks if they match
            del passw[user]#Deletes old password
            passw[user] = chgpass#Changes the password
            print "Your password has been changed."
            main(user)
    elif chgpass in maincall:
        main(user)
    elif chgpass == "back" or chgpass2 == "back":
        main(user)
        
def rootadduser(user):
    print "Input the new username>"
    nuuser = str(raw_input())#Gets new username
    if copy.count(nuuser) <1:
        if nuuser != "root" and user != "back":#Makes sure that the user isn't trying to leave.
            copy.append(nuuser)#Adds new user, and the following lines create the information about the user.
            print "Input the new password>"
            newpas = str(raw_input())
            passw[nuuser] = newpas
            rootpriv[nuuser] = 0
            admin[nuuser] = 0
            adminext[nuuser] = 0
            print "Username", nuuser, "has been created with the password", passw[nuuser],"."
            rootsys()
        elif nuuser == "back":
            rootsys()
        else:
            root(user)
    else:
        print nuuser, "is already registered as a username."
        rootadduser()
    
def root(user):
    print "Warning, system damage can be done from root mode."
    print "Hello, ",user,", you are running root mode."
    print "While in root mode, typing in \'root\' will return you to the root menu, except in certain contexts."
    print "root>"
    rootfresh = str(raw_input())
    if rootfresh == "$":
        rootothers(user)
    elif rootfresh == "%":
        rootsys(user)
    elif rootfresh == "root_dir":
        rootdir(user)
    elif rootfresh == "dir":
        rootdir(user)
    elif rootfresh == "root0":
        main(user)
    elif rootfresh == "main":
        main(user)
    elif rootfresh == "quit":
        sys.exit
    elif rootfresh == "root":
        print "You are already running in root mode."
        root(user)
    else:
        print badcommand
        root(user)

def rootothers(user):
    print "$modify_user>"
    rootselectuser = str(raw_input())
    if rootselectuser != "root" and rootselectuser != "logout" and rootselectuser not in maincall and rootselectuser in copy:
        print "$",rootselectuser,">"
        rootusercommand = str(raw_input())
        if rootusercommand == "$passchange":
            rootpasschg(user)
        elif rootusercommand == "$admin":
            rootsetadmin(rootselectuser, user)
        elif rootusercommand == "switchuser":
            del rootselectuser
            rootothers(user)
        elif rootusercommand == "$deluser":
            rootdeluser(user)
        else:
            print badcommand
            rootothers(user)
    elif rootselectuser not in copy and rootselectuser not in ("back", "#logout", "main"):
        print "That user does not exist."
        rootothers(user)
    elif rootselectuser == "#logout":
        logout(user)
    elif rootselectuser == "main":
        main(user)
    elif rootselectuser == "back":
        root(user)
    else:
        root(user)

def rootsys(user):
    print "sysadmin>"
    rootsys = str(raw_input())
    if rootsys == "%password_index":
        print passw
        gorootsys()
    elif rootsys == "%newuser":
        rootadduser()
    elif rootsys == "%deluser":
        rootdelusersys()
    elif rootsys == "root":
        root(user)
    elif rootsys == "#logout":
        logout(user)
    elif rootsys == "menu":
        menu(user)
    elif rootsys == "back":
        root(user)
    else:
        print badcommand
        rootsys(user)

def adminpasschg(user):
    print "$",adminuser,"$newpass>" 
    newpass = str(raw_input())
    newpass2 = str(raw_input("confirm>"))
    if newpass != "root" and newpass != "back":
        if newpass == newpass2 and newpass != "root":
            passw[adminuser] = newpass
            del newpass
            admin(user)
        else:
            print "Confirmed password does not match first new password input."
            admin(user)
    elif newpass == "root" or newpass2 == "root":
        admin(user)
    elif newpass == "back":
        adminothers()
    else:
        print badcommand
        admin(user)
        
        
def rootpasschg(user):
    print "$",rootselectuser,"$newpass>" 
    newpass = str(raw_input())
    newpass2 = str(raw_input("confirm>"))
    if newpass != "root" and newpass != "back":
        if newpass == newpass2 and newpass != "root":
            passw[rootselectuser] = newpass
            del newpass
            root(user)
        else:
            print "Confirmed password does not match first new password input."
            root(user)
    elif newpass == "root" or newpass2 == "root":
        root(user)
    elif newpass == "back":
        rootothers(user)
    else:
        print badcommand
        root(user)
    
def rootdelusersys(user):
    print "Input the username you wish to delete>"
    deluser = str(raw_input())
    print "Confirm the username you wish to delete>"
    deluser2 = str(raw_input())
    if deluser != "root" and deluser != "back":
        if deluser == deluser2:
            print "Are you sure you want to delete this user?"
            yorn = str(raw_input())
            if yorn in yes:
                print "Deleting user..."
                copy.remove(deluser)
                del passw[deluser]
                del admin[deluser]
                print "User removed."
                rootsys(user)
            if yorn in no:
                print "No account deleted."
                rootsys()
        else:
            print "Confirm user does not match original user given."
            rootdelusersys(user)
    elif deluser == "root":
        root(user)
    elif deluser == "back":
        rootsys(user)
    else:
        print badcommand
                
def rootdeluser(user):
    print "Confirm the username you wish to delete>"
    deluser = str(raw_input())
    if deluser != "root" and deluser != "back":
        if deluser == rootselectuser:
            print "Are you sure you want to delete this user?"
            yorn = str(raw_input())
            if yorn in yes:
                print "Deleting user..."
                copy.remove(deluser)
                del passw[deluser]
                del admin[deluser]
                print "User removed."
                rootothers(user)
            if yorn in no:
                print "No account deleted."
                rootothers(user)
        else:
            print "Confirmed user does not match original user given."
            rootdeluser(user)
    elif deluser == "root":
        root(user)
    elif deluser == "back":
        rootothers(user)
    else:
        print badcommand
        rootothers(user)
def logout(user):
        del user
        login()
def admindir(user):
    print "  Directory of commands and modules"
    print "   Modules:  $(User commands), %(System commands)"
    print ""
    print "  Answers are y or n, or yes or no."
    print "  \'#\' refers to actions that affect the current user."
    print "   dir"
    print "   admin_dir"
    print "   root_dir              (Must be in root mode)"
    print "   quit"
    print "   about"
    print "   main                  Return to the main menu."
    print "   back                  Return to the parent prompt if you are in a function."
    print "   root                  Enters root mode if you have sufficient privileges."
    print "   #passchange"
    print "   #logout"
    print "  The following commands only apply to root user only."
    print "  To gain acces to the root prompt and if you have root privileges, type in \'root\'."
    print "  \'$\' refers to root commands that affect other users."
    print "  If applicable, type and enter \'$\' before typing in the username you wish to modify. Enter the username, and one of the following commands."
    print "  \'%\' refers to system changes. Use it the same way as \'$\'."
    print "   A \\ separates each command from its module, if applicable."
    print "   main                  logs out of admin mode."
    print "   back                  Returns you to the parent prompt if you are in a function."
    print "   $\\$passchange        Resets the password"
    print "   $\\$admin or $admin   Entering a 1 or a 0 following this command gives admin privileges or removes them, respectively."
    print "   $\\$rights            Press enter, and followed with the name of a program appended with a 0 or a 1 to give rights to use the program."
    print "   $\\switchuser         For changing the target user while in \'$\'."
    print "   %\\%password_index    Lists each username and their passwords."
    print "   %\\%newuser           Creates a new user."
    admin()
def rootdir(user):
    print "  Directory of commands and modules"
    print "   Modules:  $(User commands), %(System commands)"
    print ""
    print "  Answers are y or n, or yes or no."
    print "  \'#\' refers to actions that affect the current user."
    print "   dir"
    print "   admin_dir"
    print "   root_dir              (Must be in root mode)"
    print "   quit"
    print "   about"
    print "   main                  Return to the main menu."
    print "   back                  Return to the parent prompt if you are in a function."
    print "   root                  Enters root mode if you have sufficient privileges."
    print "   #passchange"
    print "   #logout"
    print "  The following commands only apply to root user only."
    print "  To gain acces to the root prompt and if you have root privileges, type in \'root\'."
    print "  \'$\' refers to root commands that affect other users."
    print "  If applicable, type and enter \'$\' before typing in the username you wish to modify. Enter the username, and one of the following commands."
    print "  \'%\' refers to system changes. Use it the same way as \'$\'."
    print "   A \\ separates each command from its module, if applicable."
    print "   root                  To return to the root menu at any point."
    print "   root0                 Deactivates root mode. Must be done from main root prompt."
    print "   main                  Same effect as root0"
    print "   back                  Returns you to the parent prompt if you are in a function."
    print "   $\\$passchange        Resets the password"
    print "   $\\$admin or $admin   Entering a 1 or a 0 following this command gives admin privileges or removes them, respectively."
    print "   $\\$rights            Press enter, and followed with the name of a program appended with a 0 or a 1 to give rights to use the program."
    print "   $\\$deluser           Delete user."
    print "   $\\switchuser         For changing the target user while in \'$\'."
    print "   %\\%password_index    Lists each username and their passwords."
    print "   %\\%newuser           Creates a new user."
    print "   %\\%deluser           Same effect as $deluser"
    root(user)
    
def dir(user):
    print "  Directory of commands and modules"
    print "  answers are y or n, or yes or no."
    print "  \'#\' refers to actions that affect the current user."
    print "   dir"
    print "   admin_dir"
    print "   quit"
    print "   about"
    print "   main                  Return to main menu."
    print "   back                  Return to the parent prompt if you are in a function."
    print "   root                  Enters root mode if you have sufficient privileges."
    print "   #passchange"
    print "   #logout"
    main(user)
    
def gorootsys():
    rootsys()
def goroot():
    root(user)
def rootsetadmin(rootselectuser, user):
    print "admin_priv>"
    adminpriv = str(raw_input())
    adminpri[rootselectuser] = adminpriv
    del adminpriv
    root(user)
#In case you are completely dense, this next command tells the program to run the login module.
#Uncomment the following line for the program to work correctly
login()
#root("Daniel") Comment this line out for the program to work correctly. For root testing only.
