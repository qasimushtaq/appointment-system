# Import libraries/packages.
import os
import datetime
import pyinputplus as pyip
from tabulate import tabulate
import gspread
from google.oauth2.service_account import Credentials

# Define the APIs used by the program.
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("appointment-system")

# Global variables for app processes.

# Variable for sheet in the spreadsheet.
APPTS = SHEET.worksheet("appointments")
# Stores the current date.
CURRENT_DATE = datetime.date.today()
# Places and stores the current date into the correct format for when required.
CURRENT_DATE_FMTED = datetime.datetime.strftime(CURRENT_DATE, "%d/%m/%Y")

def main_menu():
    """
    Displays the main menu options for the user
    to select in order to navigate the application.
    """
    clear_tmnl()
    print("Appointment System - Main menu\n")
    print("Please select an option below.\n")

    print("(1) Book new appointment.")
    print("(2) View today's appointments.")
    print("(3) Search appointments.")
    print("(4) Cancel appointment.")
    print("(5) View application instructions.")

    while True:
        main_menu_ans = input("\n")
        if main_menu_ans not in ("1", "2", "3", "4", "5"):
            print("Invalid input.")
            print("Please choose an option between 1 and 5.")
        else:
            break

    if main_menu_ans == ("1"):
        collect_details()
    elif main_menu_ans == ("2"):
        search_date("today")
    elif main_menu_ans == ("3"):
        search_menu()
    elif main_menu_ans == ("4"):
        cancelation_prompt()
    elif main_menu_ans == ("5"):
        app_info()
       
def search_menu():
    """
    Displays options to search by date, by name, or return to the main menu.
    """
    clear_tmnl()
    print("Appointment Syatem - Search Menu\n")
    print("What would you like to do?\n")

    print("(1) Search appointments by name.")
    print("(2) Search appointments by date.")
    print("(3) Return to main menu.")

    while True:
        search_ans = input("\n")
        if search_ans not in ("1", "2", "3"):
            print("Invalid input.")
            print("Please choose an option between 1 and 2.")
        else:
            break

    if search_ans == ("1"):
        search_name("view")
    elif search_ans == ("2"):
        search_date("search")
    elif search_ans == ("3"):
        main_menu()

def app_info():
    """
    Provides the user with instructions on how to use the app.
    Once the user has read and is satisfied, they may press enter
    to return to the main menu.
    """
    clear_tmnl()

    print("To book an appointment:")
    print("1 - Select option '(1)' in the menu.")
    print("2 - Enter the details that are requested, one by one.")
    print("3 - Confirm the details to book or cancel the booking.")
    print("NB - Enter 'Exit' when entering details to stop/return to menu.\n")

    print("To view today's appointments, select option '(2)' in the menu.\n")

    print("To search for specific appointments:")
    print("1 - Select option '(3)' in the menu to go to the search menu.")
    print("2 - Select between options to search for a name or a date.")
    print("3 - Enter the name/date you wish to search for.")
    print("4 - View the results of your search.\n")

    print("To cancel an appointment:")
    print("1 - Select option '(4)' in the menu.")
    print("2 - Enter the name and surname you wish to cancel for, one by one.")
    print("3 - Provide final confirmation to cancel the appointment.")
    print("NB - Enter 'Exit' when entering details to stop/return to menu.\n")

    input("Press enter to return to menu\n")
    main_menu()
