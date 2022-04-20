#This script contains functions for validating user input
#Matt Curtin 4/7/2022

#Email validation
from validate_email import validate_email as ve

#Regex for matching patterns
import re


#Function for validating name
#Input: name (string)
#Output: True if valid, False if not
#Name is valid if
#   Letters an numbers
def validate_name(name):
    #define password regex
    regex = "^[A-Za-z ]{1,30}$"
    pattern = re.compile(regex)

    #Match password to pattern
    match = re.search(pattern, name)

    if match is not None:
        return True

    return False

#Function for validating passwords
#Input: password (string)
#Output: True if valid, False if not
#Password is valid if it is
#   8 -> 20 characters long
#   contains: >= 1 uppercase
#   contains >=1 lowercase
#   contains >= number
#   contains >= special character
#Reference:
#   https://www.geeksforgeeks.org/password-validation-in-python/
def validate_password(password):
    #define password regex
    regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
    pattern = re.compile(regex)

    #Match password to pattern
    match = re.search(pattern, password)

    if match is not None:
        return True

    return False

#Function for validating address
#Input: address (string)
#Output: True if valid, False if not
#Address is valid if
#   Exists in the real world
def validate_address(address):
    
    return True

#Function for validating usernames
#Note: This does not test if username already exists in system. Just that it is correctly formatted
#Input: username (string)
#Output: True if valid, False if not
#Username is valid if
#   Length > 3
#   Alphanumeric
def validate_username(username):
    #define username regex
    regex = "^[A-Za-z\d@$!#%*?&]{3,20}$"
    pattern = re.compile(regex)

    #Match password to pattern
    match = re.search(pattern, username)
    
    if match is not None:
        return True

    return False

#Function for validating email addresses
#Note: This does not test if email already exists in system. Just that it is correctly formatted
#Input: email (string)
#Output: True if valid, False if not.
#Reference:
#   https://pypi.org/project/py3-validate-email/
def validate_email_address(email):
    
    #User py3-validate-email function 
    #Checks format is okay
    #Checks if domain is on blacklist - spam emails
    #Checks if domain exists on DNS and has record 
    valid = ve(email, check_smtp=False)

    if valid:
        return True

    return False