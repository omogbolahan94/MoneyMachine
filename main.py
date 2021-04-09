from datetime import datetime
import random
import sys
import json


# database is a global variable
database = {}


# read data function
def read_data_only():
    """
    this data is loaded to authenticate login
    :return:
    """
    global database
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        pass
    else:
        with open("data.json", "r") as file:
            database = data


def data_handler(new_data):
    """
    This data is loaded or updated or created for a newly registered user
    :param new_data:
    :return:
    """
    global database
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        # if file does not already exist, dump new data into the data.son file
        with open("data.json", "w") as file:
            json.dump(new_data, file, indent=4)
        # load the data and assign it to database
        with open("data.json", "r") as file:
            data = json.load(file)
            database = data
    else:
        # update old data with new data
        data.update(new_data)
        # re-assign updated data to global database variable
        database = data
        with open("data.json", "w") as file:
            # dump the updated json data into the data.json file
            json.dump(data, file, indent=4)


def try_again():
    choice = int(input("Do You Want To Perform Another Transaction? 1(Try Again), 0(exit): "))
    if choice == 0:
        print("Thank You For Banking With Us. Bye!")
        return False
    elif choice == 1:
        return True
    else:
        print("Invalid Option! Please Enter A Valid Option.")
        return True


def bank_operations(user_account_number):
    print("*" * 20)
    print(f"Welcome {database[user_account_number]['firstName']} {database[user_account_number]['lastName']}.")
    print("*" * 20)

    operations = True
    while operations:
        print("There Are Four(4) Available Options: ")
        print("1: Withdraw")
        print("2: Cash Deposit")
        print("3: Logout")
        print("4: Exit")

        if user_account_number in database.keys():
            selected_option = int(input("Please Select A Valid Option: "))
            if selected_option == 1:
                withdrawal_amount = withdrawal()
                if database[user_account_number]["accountBalance"] < withdrawal_amount:
                    print("Insufficient Fund!")
                    operations = try_again()
                else:
                    database[user_account_number]["accountBalance"] -= withdrawal_amount
                    print("Take Your Cash")
                    operations = try_again()

            elif selected_option == 2:
                deposit_amount = deposit()
                database[user_account_number]["accountBalance"] += deposit_amount
                print(f"Balance: {database[user_account_number]['accountBalance']}")
                operations = try_again()

            elif selected_option == 3:
                print("Thank you for contacting us")
                logout()

            elif selected_option == 4:
                sys.exit("Thank You For Banking With Us. Bye!")

            else:
                print("Invalid Option Selected, Please Try Again.")
                bank_operations(user_account_number)

    try:
        with open( "data.json", "r" ) as file :
            data = json.load(file)
    except FileNotFoundError:
        pass
    else:
        # update database due to banking operations
        data.update(database)
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)


def register():
    """

    :return:
    """
    print("\n")
    print("*" * 5, "REGISTER", "*" * 5)
    email = input("What is your email address? ")
    first_name = input("What is your first name? ")
    last_name = input("What is your last name? ")
    password = input("Create a password: ")
    account_number = generate_account_number()
    account_balance = 0

    new_data = {}
    new_data[account_number] = {"firstName": first_name, "lastName": last_name,
                                "email": email, "password": password, "accountBalance": account_balance}

    data_handler(new_data)

    print("\n")
    print("*" * 10, "Hurray! Your Account Has Been Created", "*" * 10)
    print(f"Your Account Number Is: {account_number}")


def login():
    """

    :return:
    """
    print( '\n' )
    global database
    read_data_only()

    print("\n")
    print("*" * 5, "LOGIN", "*" * 5)
    account_number = input("Enter your Account Number: ")
    password = input("Enter Your Password: ")

    if account_number in database.keys() and password == database[account_number]["password"]:
        bank_operations(account_number)
    else:
        choice = int(input(f"Your Data Is Not Present In Our DataBase. "
                           f"May Be You Should Create An Account: 1(To Try Login In Again), 2(To Register), 0(exit): "))
        if choice == 1:
            login()
        elif choice == 0:
            sys.exit("Thank You For Banking With Us. Bye!")
        elif choice == 2:
            init()
        else:
            print( "Invalid Account or Password. Please Ensure You Log In Correct Details." )


def generate_account_number():
    """

    :return:
    """
    generated_number = random.randrange(1111111111, 9999999999)
    return generated_number


def logout():
    """
    logout the banking system
    :return:
    """
    init()


def withdrawal():
    """
    withdraw cash
    :return:
    """
    amount = float(input("How much would you like to withdrawal? "))
    return amount


def deposit():
    """
    deposit a certain amount into the bank
    :return:
    """
    deposit_amount = float(input('How much would you like to deposit? '))
    return deposit_amount


def init():
    """
    This function starts our banking operation
    :return:
    """
    print('\n')
    print("#"*10, "WELCOME TO PYTHON BANK", "#"*10)
    print(f"Current Date-Time: {datetime.now()}")

    have_account = int(input("Do You Have An Account With Us: 1(To Log In), 2(To Register An Account), 0(To Exit): "))

    if have_account == 1:
        login()

    elif have_account == 2:
        register()
        correct_option = True
        while correct_option:
            transact = int(input("Do You Want To Make Your First Transaction? 1(Make Transaction) or 0(Exit): "))
            if transact == 1:
                correct_option = False
                login()
            elif transact == 0:
                sys.exit("Thank You For Banking With Us. Bye!")
            else:
                print("Please Choose A valid Option.")

    elif have_account == 0:
        sys.exit("Thank You For Banking With Us. Bye!")

    else:
        print("You Have Selected An Invalid Option.")
        init()


############# INITIALIZZING BANKING ##############
init()
