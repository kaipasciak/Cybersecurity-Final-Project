CS 2660 OL Final Project
Spring 2024
Author: Kai Pasciak

Program Overview:

To create an enhanced version of the intranet system created in the first lab assignment, I have used
the files from the Catamount Community Bank as a framework. Instead of the lessons being listed on the
home page, I have the menu options listed. When no user is logged in, the permission level is set to
the baseline, and the option to log in or register as a new user is listed at the bottom of the menu.
When a user is logged in, their permission level from the database will be stored by the program.
Additionally, stored passwords will be salted and other security vulnerabilities such as SQL injections
will have measures in place to prevent them.

Process:

The first step was to update bank.py to include functions for each menu item, as well as for successful
log ins and other actions that can be taken. The config file now has a link to my silk server where
a json file stores the active menu items where it used to have Jim Eddy's lessons. Any of the keys
in the catalog dictionary with "true" listed next to them in the json file will be listed as options
selected from the "CATALOG" dictionary in config.py to be added to the "display" dictionary. "display" is
imported to bank.py from config.py for the flask application. To create the database, run setup.py to run the SQL
create statement for the table and insert the first few lines into it. Anytime you want to get rid of users you've added
since running setup.py, just run setup.py again. Bank.py is the flask app and running werk.py runs the whole system of
files.

Rather than having the user's id be a variable part of the URL, it is now stored in the flask program
so that somebody with malicious intent can't input any URL to get any customer's information. When
logged out, the user ID and permission level will both be set to 0 and username will be set to "guest".

These are the example accounts created in the database
'john_doe', 'Password123$', 0
'jane_smith', 'Secret456?', 1
'admin', 'Admin123!', 2

Test each user with their different access levels. Each user will be able to view different menu options. They may be
met with a page that says they aren't allowed to view it.

There's functionality to register a new user with a permission level equal to the guest user. The program will not allow
the user to use a duplicate username or a password that isn't within the required standards. It will give the option to the
user to generate a password. The generate strong password function calls itself until it comes up with a password that
satisfies the conditions. Stored passwords are salted to prevent attackers viewing them without knowing the salt. An SQL insert statement
is required to put the username into the database when registering a new user. The input is sanitized to prevent SQL injections.

Many programs from the community bank folder are still included in this because they are required to set up the whole system. My work is as
detailed in this README file. Additions were made to config.py to include the menu items of lab assignment 1. Setup.py was modified to
create the table and database in the directions. Password_crack.py was modified to salt and hash passwords. Bank.py was modified to
include functions for every menu item as well as successful logins (already included), restricted access, and generating strong passwords.
Accounts.db can be deleted to run setup.py again to start it over with only the original three users. Catalog.json was created and
SFTPed to my silk server to allow the menu items to be displayed the same way they were in the original Catamount bank. Werk.py is unchanged
and is just for the flask app.

 Citations:
 - Catamount Community Bank files

