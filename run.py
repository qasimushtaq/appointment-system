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

