import sys
copy = ["Daniel", "Oliver"]
passw = {"Daniel": "Feathers", "Oliver": "Cat"}
admin = {"Daniel": 1, "Oliver": 0}
passchgpriv = {"Daniel": 1}
nul = 0
rootpriv = {"Daniel": 1, "Oliver": 0}
badcommand = "Unrecognized command"

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
        newu = str(raw_input("Would you like to make a new user? y/n> "))
        if newu in ("y", "Y", "yes", "Yes"):
            user = str(raw_input("Input your new username>"))
            copy.append(user)
            newpas = str(raw_input("Input your new password>"))
            passw[user] = newpas
            login()
        elif newu in ("n", "N", "no", "No"):
            print "Very well."
            login()            
        else:
            print badcommand
            login()
            
#Define the main body of the program
def main(user):
    print "Hello, ",user
    print "Type Dir for help."
    #Add a prompt
    prompt = str(raw_input("prompt>"))
    #Checks for various recognized commands
    if prompt in ("dir", "Dir", "Help", "help"):
        dir()
    elif prompt == "about":
        print "This program was aimed to imitate a fully working operating system. \nThe project was started by Daniel Ralston, a tenth grade student, in November \n2007 as a way to teach himself the Python Programming Language."
        main(user)
    elif prompt == "#passchange":
        if passchgpriv[user] == 1:
            passchgbool(user)
        else:
            print "You do not have sufficient privileges to change your password."
            main(user)
    elif prompt == "logout":
        del user
        login()
    elif prompt == "root" and rootpriv[user] == 1:
        root(user)
    else:
        print badcommand
        main(user)

def passchgbool(user):
    #Asks if the user really wants to change his password
    chgbool = str(raw_input("Do you want to change your password?" ))
    if chgbool in ("Yes", "yes", "Y", "y"):
        #If yes, go to passchange
        passchange(user)
    elif chgbool in ("No", "no" "N", "n"):
        #if not, go to main
        main(user)
    else:
        print badcommand
        
def passchange(user):
    chgpass = str(raw_input("new_password>"))
    chgpass2 = str(raw_input("confirm>"))
    if chgpass == chgpass2:
        del passw[user]
        passw[user] = chgpass
        main(user)
    elif chgpass in ("Menu", "menu", "Main", "main"):
        main(user)
        
def adduser():
    print "Input the new username>"
    user = str(raw_input())
    copy.append(user)
    print "Input the new password>"
    newpas = str(raw_input())
    passw[user] = newpas
    rootpriv[user] = 0
    admin[user] = 0
    login()
    
def root():
    print "Warning, system damage can be done from the root user."
    print "root>"
    rootfresh = str(raw_input())
    if rootfresh == "$":
        rootothers()
    elif rootfresh == "%":
        rootsys()
    elif rootfresh == "root_dir":
        rootdir()
    elif rootfresh == "dir":
        dir()
        rootdir()
    else:
        print badcommand
        root()
        
def rootothers():
    print "$user>"
    rootselectuser = str(raw_input())
    print "$",rootselectuser,">"
    rootusercommand = str(raw_input())
    if rootusercommand == "$passchange":
        print "$",rootselectuser,"$newpass>" 
        newpass = str(raw_input())
        newpass2 = str(raw_input("confirm>"))
        if newpass == newpass2:
            passw[rootselectuser] = newpass
            del newpass
            root()
        else:
            print "Confirmed password does not match first new password input."
            root()
    else:
        print badcommand
        root()
def rootsys():
    print "sysadmin>"
    
    
def dir():
    print "  Directory of commands and modules"
    print "  answers are y or n, or yes or no. Capitalization counts. "
    print "  \'#\' refers to actions that affect the current user."
    print "   dir"
    print "   admin_dir"
    print "   root_dir"
    print "   about"
    print "   #passchange"
    print "   #logout"
    main(user)
    
def rootdir():
    print "  Directory of commands and modules"
    print "  answers are y or n, or yes or no. Capitalization counts. "
    print "  \'#\' refers to actions that affect the current user."
    print "   dir"
    print "   admin_dir"
    print "   root_dir              (Must be in root mode)"
    print "   about"
    print "   #passchange"
    print "   #logout"
    print "  The following commands only apply to root user only."
    print "  To gain acces to the root prompt and if you have root privileges, type in \'root\'."
    print "  \'$\' refers to root commands that affect other users."
    print "  If applicable, type and enter \'$\' before typing in the username you wish to modify. Enter the username, and one of the following commands."
    print "  \'%\' refers to system changes. Use it the same way as \'$\'."
    print "   $passchange           Resets the password"
    print "   $admin1 or $admin0    Gives admin privileges or removes them, respectively."
    print "   $rights               Press enter, and followed with the name of a program appended with a 0 or a 1 to give rights to use the program."
    print "   %password_index"
    print "   %newuser"
    root()
#In case you are completely dense, this line tells the program to run the login module.
root()