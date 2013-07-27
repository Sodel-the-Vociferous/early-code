remembered = ["Daniel", "Oliver"]
copy = remembered [:]
nul = 0


def login():
    user = str(raw_input("login> "))
    if copy.count(user) > nul:
        print "Hello, ", user
    else:
        print "I don't recognize you."
        b = str(raw_input("Would you like to create a new username? "))
        if b == "Yes" or b == "yes" or b== "y":
            copy.append(user)
            print "Your new user file has been created."
            login()
        else:
            print "Very well."
            login()

login()