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

def collect_details():
    """
    Collects the patient's details from other functions
    and adds them to a list that can be appended to the
    appointments sheet after being checked and confirmed.
    """
    clear_tmnl()
    appt_categories = APPTS.row_values(1)
    appt_detail = dict.fromkeys(appt_categories)

    appt_detail["Date"] = get_date("book")
    appt_detail["Time"] = get_time(appt_detail["Date"])
    appt_detail["Name"] = get_name("f_name")
    appt_detail["Surname"] = get_name("l_name")

    appt_details = list(appt_detail.values())
    existing_appt_check = check_existing_appts(appt_details)
    if existing_appt_check:
        clear_tmnl()
        print("A booking for this patient already exists on this date.")
        print("You can only book one appointment per day per patient.\n")
        book_again_prompt("terminated")
    else:
        confirm_appointment(appt_details)

def get_date(reason):
    """
    Gets the date input from the user and validates that it is in the correct
    format, and depending on the argument provided, is not a past date and,
    is available for booking. Requests input until it is valid or returns
    to menu if 'Exit' is input.
    """
    clear_tmnl()
    print("Please enter an appointment date in the format of dd/mm/yyyy.")

    while True:
        date_input = input("\n").capitalize()
        if date_input == "Exit":
            main_menu()
            break
        else:
            try:
                date_fm = datetime.datetime.strptime(date_input,
                                                     "%d/%m/%Y").date()
            except ValueError:
                print("Invalid input, a date should:\n")
                print("- Be in the format of dd/mm/yyyy.")
                print("- Contain realistic values for day, month and year.\n")
                print("Please input a valid date.")
            else:
                if reason == "book":
                    date_available = bool(get_avail_times(date_input))
                    if date_available is False:
                        print(f"Sorry, {date_input} is unavailable.")
                        print("Please enter a new date.")
                    else:
                        if CURRENT_DATE > date_fm:
                            print("Invalid date input (past date).\n")
                            print("Please enter a present or future date.")
                        else:
                            break
                elif reason == "search":
                    break

    return date_input

def get_time(data):
    """
    Provides list options of available times and requests input for desired
    time. If only one time is available it prompts the user to continue or
    enter a new date. Requests input until it is valid or returns to menu
    if 'Exit' is input.
    """
    clear_tmnl()
    times = get_avail_times(data)
    if len(times) == 1:
        print(f"The only available time on {data} is {times[0]}.\n")
        print("Press 1 to continue with this time or 2 to enter a new date.")
        while True:
            time_ans = input("")
            if time_ans not in ("1", "2"):
                print("Invalid input.\n")
                print("Please choose an option between 1 and 2.")
            else:
                break
        if time_ans == "1":
            time_input = times[0]
            return time_input
        else:
            collect_details()

    else:
        print(f"Below is a list of available times for {data}.\n")
        time_input = pyip.inputMenu(times,
                                    prompt="Select a time from the list.\n",
                                    numbered=True,
                                    allowRegexes=[("Exit"), ("exit")]
                                    )
        if time_input.capitalize() == "Exit":
            main_menu()
        else:
            return time_input
def get_avail_times(data):
    """
    Gets return value from get_appts_for_date function for booked times
    and removes them from the appointment times list to create a list of
    available times and returns the available times. If the current date
    is input, past times are removed from available times.
    """
    appt_times = ["0800",
                  "0900",
                  "1000",
                  "1100",
                  "1200",
                  "1400",
                  "1500",
                  "1600"
                  ]
    unav_times = get_appts_for_date(data, "booked_times")
    av_times = [time for time in appt_times if time not in unav_times]
    if data == CURRENT_DATE_FMTED:
        current_time = datetime.datetime.now().strftime("%H%M")
        today_av_times = [time for time in av_times if time > current_time]
        return today_av_times
    else:
        return av_times
def get_name(name_part):
    """
    Gets the name input from the user and validates that it contains
    only letters, no spaces, and is at least 2 letters in length.
    If the user inputs 'Exit', it returns them to the main menu.
    Input is requested until it is valid.
    """
    clear_tmnl()
    if name_part == ("f_name"):
        name_prompt = "first name"
    elif name_part == ("l_name"):
        name_prompt = "surname"

    print(f"Please enter the patient's {name_prompt}.")

    while True:
        pat_name = input("\n").capitalize()
        if pat_name.isalpha() and len(pat_name) > 1:
            break
        else:
            print("Invalid input, a name must contain:\n")
            print("- At least 2 letters.")
            print("- Only letters.")
            print("- No spaces.\n")
            print(f"Please enter a valid {name_prompt}.")

    if pat_name == "Exit":
        main_menu()
    else:
        return pat_name
def check_existing_appts(details):
    """
    Checks the appointment records for the name and date provided
    and if a booking already exists for the details, returns true,
    otherwise, it returns false.
    """
    detail_date = details[0]
    detail_name = details[2:4]
    date_bookings = get_appts_for_date(detail_date, "bookings")

    # Idea on how to implement check came from stackoverflow.
    # (Link in the readme)
    existing_appt = None
    for booking in date_bookings:
        for i in range(len(booking) - len(detail_name) + 1):
            if detail_name == booking[i:i+len(detail_name)]:
                existing_appt = True

    return existing_appt

def confirm_appointment(data):
    """
    Presents the user with the appointment details entered
    and asks for final confirmation to make the booking
    or cancel. Input is requested until a valid option
    is input.
    """
    clear_tmnl()
    appt_headers = ["Date", "Time", "Name", "Surname"]
    print("Please confirm the following details before booking.\n")
    print(tabulate([data], headers=appt_headers, tablefmt="fancy_grid"))
    print("Enter Y to confirm or N to cancel.\n")
    print("WARNING!")
    print("Entering N will cancel the appointment and data will be lost.")

    while True:
        confirmation = input("\n").capitalize()
        if confirmation not in ("Y", "N"):
            print("Please input a valid option (Y/N).")
        else:
            break

    if confirmation == ("Y"):
        update_appts(data)
        book_again_prompt("booked")
    elif confirmation == ("N"):
        clear_tmnl()
        print("Booking terminated.\n")
        book_again_prompt("terminated")

def update_appts(data):
    """
    Updates the appointments sheet using the data provided.
    """
    print("Updating appointments...\n")
    APPTS.append_row(data, value_input_option='USER_ENTERED')
    print("Appointment booked successfully!")
    sort_sheet()