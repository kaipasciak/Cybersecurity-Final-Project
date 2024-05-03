"""
Flask app configuration
"""
import requests

DEBUG = True
SC = ";"
TEMPLATES_AUTO_RELOAD = True
DB_FILE = './instance/var/db/test.db'
SECRET_KEY = 'This is not very secret, is it?'
CREDENTIALS_FILE = 'instance/static/passwd'  # Ack! This is web-accessible!
CATALOG = {
    "Accounting": [".accounting", "Accounting"],
    "Time Reporting": [".time", "Time Reporting"],
    "IT Helpdesk": [".it", "IT Helpdesk"],
    "Engineering Documents": [".engineering", "Engineering Documents"],
    "Log In": [".login", "Customer Log In"],
    "Log Out": [".logout", "Log Out"],
    "Register New User": [".register", "Register New User"]
}
display = {}
response = requests.get("https://kpasciak.w3.uvm.edu/catalog.json")
active = response.json()
for key in active:
    if active[key]:
        display[key] = CATALOG[key]



