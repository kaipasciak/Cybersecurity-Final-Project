"""
CS 2660 Final Project
Author: Kai Pasciak

A significant portion of the following code is from this class' Catamount Community Bank files.
"""


import csv
import sqlite3
from config import display
from flask import Flask, render_template, request, url_for, flash, redirect
from db import Db
from lessons import sql_injection
from lessons.password_crack import hash_pw, authenticate
import string
import random

app = Flask(__name__, static_folder='instance/static')

app.config.from_object('config')

# Create variables to store the user id and access level
# User ID is an integer stored in the SQL database
userId = -1

# Username is a string that can be displayed on the website
user = ""

# Permission is an integer with a value of either 0, 1 or 2
# 0: IT, 1: Time reporting, 2: Accounting, Engineering Documents
permission = 0

# Dictionary for storing user data
permissions = {}

# Dictionary to keep track of incorrect password attempts
incorrect = {}

# Home page displays username or guest
@app.route("/", methods=['GET', 'POST'])
def home():
    """Home page """
    return render_template('home.html',
                           title="Home Page",
                           heading="Home Page",
                           show=display,
                           id=userId,
                           u=user)


# Time Reporting Option available to levels 1 and 2
@app.route("/time", methods=['GET'])
def time():
    """ Time Reporting Page """
    if permission > 0:
        return render_template('time.html')
    return render_template('restricted.html')


# Accounting Option available to level 2 only
@app.route("/accounting", methods=['GET'])
def accounting():
    """ Accounting Page """
    if permission == 2:
        return render_template('accounting.html')
    return render_template('restricted.html')


# IT Helpdesk Option available to all levels
@app.route("/it", methods=['GET'])
def it():
    """ IT Helpdesk Page """

    return render_template('it.html')


# Engineering Documents Option available to levels 1 and 2
@app.route("/engineering", methods=['GET'])
def engineering():
    """ Engineering Documents Page """
    if permission > 0:
        return render_template('engineer.php')
    return render_template('restricted.html')

# Log In Option
@app.route("/login", methods=['GET', 'POST'])
def login():
    """ Login the user """

    global user
    global permission
    global userId

    # -1 is the userId value indicating a guest user
    if userId != -1:
        flash("Already logged in!")
        return render_template('home.html',
                               title="Home Page",
                               heading="Home Page",
                               show=display,
                               id=userId,
                               u=user)

    # Connect to database and put rows into below dictionary
    global permissions
    global incorrect

    # Load user data into permissions dictionary
    try:
        conn = sqlite3.connect('accounts.db')
        c = conn.cursor()
        for row in c.execute("SELECT * FROM accounts"):
            permissions[row[1]] = [row[0], row[2], row[3]]
    except sqlite3.DatabaseError:
        print("Error. Could not retrieve data.")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


    if request.method == 'POST':
        username = request.form.get('username').lower()
        password = request.form.get('password')
        pw_hash = hash_pw(password)

        try:
            if authenticate(permissions[username][1], password):
                try:
                    if incorrect[username] == 3:
                        flash("Locked out of account!")
                        return render_template('home.html',
                                        title="Home Page",
                                        heading="Home Page",
                                        show=display,
                                        id=userId,
                                        u=user)
                except KeyError:
                    pass

                user = username
                userId = permissions[username][0]
                permission = permissions[username][2]

                # If correct login, set incorrect value to 0
                incorrect[username] = 0
                return redirect(url_for('login_success',
                                        id_=permissions[username][0]))
            else:
                # Keep track of number of incorrect attempts
                if username in incorrect:
                    # Lock user out after 3 incorrect attempts
                    if incorrect[username] == 3:
                        flash("Locked out of account!")
                        render_template('home.html',
                                        title="Home Page",
                                        heading="Home Page",
                                        show=display,
                                        id=userId,
                                        u=user)
                    elif incorrect[username] < 3:
                        incorrect[username] += 1

                # If first incorrect log in, put username in dict and set value to 1
                else:
                    incorrect[username] = 1

        except KeyError:
            pass

        flash("Invalid username or password!", 'alert-danger')
    return render_template('login.html',
                           title="Secure Login",
                           heading="Secure Login")
# Log Out Option
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    """ Log Out Page """

    global user, permission, userId
    user = ""
    permission = 0
    userId = -1
    flash("You have logged out!", 'alert-success')
    return render_template('home.html',
                           title="Home Page",
                           heading="Home Page",
                           show=display,
                           id=userId,
                           u=user)

# Register New User Option
@app.route("/register", methods=['GET', 'POST'])
def register():
    """ Register New User Page """
    global newPassword
    if userId != -1:
        flash("Please log out before registering a new user!")
        return render_template('home.html',
                           title="Home Page",
                           heading="Home Page",
                           show=display,
                           id=userId,
                           u=user)

    # This is generated in this function rather than generate so that it doesn't change between POST requests
    newPassword = generate_strong_password()

    if request.method == 'POST':
        newUsername = request.form.get('username').lower()
        newPassword = request.form.get('password')
        newPassword2 = request.form.get('password2')
        print(newUsername, newPassword, newPassword2)

        # Input validation
        # Check for existing user
        for i in permissions:
            if newUsername == i:
                # Duplicate username found
                flash("Username already in use!")
                return render_template('register.html')

        # Check if passwords match
        if newPassword != newPassword2:
            flash("Passwords must match!")
            return render_template('register.html')

        # Check strength
        if password_strength(newPassword) == False:
            flash("Password not complex enough")
            return render_template('register.html')

        # Add to database
        add_user(newUsername, newPassword)

        # Success message
        flash("New user successfully registered!")
        return render_template('home.html',
                               title="Home Page",
                               heading="Home Page",
                               show=display,
                               id=userId,
                               u=user)

    return render_template('register.html')

# Strong password generating option
@app.route("/generate", methods=['GET', 'POST'])
def generate():
    """ Generate a strong password """
    global newPassword

    if request.method == 'POST':
        newUsername = request.form.get('username').lower()

        # Check if username is in use
        for i in permissions:
            if newUsername == i:
                # Duplicate username found
                flash("Username already in use!")
                return render_template('register.html')

        # Add to database
        add_user(newUsername, newPassword)

        # Success message
        flash("New user successfully registered!")
        return render_template('home.html',
                               title="Home Page",
                               heading="Home Page",
                               show=display,
                               id=userId,
                               u=user)


    return render_template('generate.html',
                           password = newPassword)

def add_user(username, password):
    """ Add a user, user ID, hashed password and access level to a row in the database """

    # Close all double or single quotes
    new_username = username.replace('"', '""')
    new_username = new_username.replace("'", "''")

    # Get rid of percent signs
    new_username = new_username.replace("%", "")
    print("Adding new user", username, password)


    data_to_insert = [(username, hash_pw(password), 0)]
    try:
        conn = sqlite3.connect('accounts.db')
        c = conn.cursor()
        c.executemany("INSERT INTO accounts (username, password, accessLevel) VALUES (?, ?, ?)", data_to_insert)
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error. Tried to add duplicate record!")
    else:
        print("Success")
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()


def generate_strong_password():
    """ Generate a strong password """

    # Characters is a string that holds all letters, numbers and special characters
    characters = ""
    characters += string.ascii_letters + string.digits + "!@#$%^&*"
    password = ""
    for i in range(20):
        password += random.choice(characters)

    # Call itself until the generated password satisfies requirements
    if password_strength(password) == False:
        password = generate_strong_password()
    return password

def password_strength(test_password) -> bool:
    """
    Check basic password strength. Return true if password
    meets minimum complexity criteria, false otherwise.

    :param test_password: str
    :return: bool
    """

    SPECIAL_CHAR = "!@#$%^&*"

    if test_password.isalnum() or test_password.isalpha():
        return False
    if len(test_password) < 8:
        return False
    if len(test_password) > 25:
        return False
    special_char_check = False
    has_upper = False
    has_lower = False
    has_digit = False
    for ch in test_password:
        if ch in SPECIAL_CHAR:
            special_char_check = True
        if ch.isupper():
            has_upper = True
        if ch.islower():
            has_lower = True
        if ch.isdigit():
            has_digit = True
    if not special_char_check or \
            not has_upper or \
            not has_lower or \
            not has_digit:
        return False
    else:
        return True

@app.route("/login_success/<int:id_>", methods=['GET', ])
def login_success(id_):
    flash("Welcome! You have logged in!", 'alert-success')
    return render_template('home.html',
                           title="Customer Home",
                           heading="Customer Home",
                           show=display,
                           id=userId,
                           u=user)


@app.route("/hashit", methods=['GET', ])
def hashit():
    """Hash a password. DON'T EVER DO THIS LIKE THIS IN THE REAL WORLD! """
    pw = request.args.get('pw')
    salt = request.args.get('salt')
    if salt is None:
        salt = ''
    return hash_pw(pw, salt)
