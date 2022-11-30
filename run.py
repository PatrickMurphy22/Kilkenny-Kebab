import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("kilkenny_kebab")


def home_screen():
    """
    This function welcomes the user to the home
    screen of Kilkenny Kebab. Then it
    instructes the user on how to progress.
    """
    print("Welcome to Kilkenny Kebab.")
    print("We were voted Ireland's No.1 Kebab shop in 2022. ")
    print("To view our menu's please enter the menu's name below.\n")


def menu_selection():
    """
    This function will allow users to select either the menu
    they wish to view, or their current basket.
    """
    print("Menu options: - Food - Sides - Drinks - Basket -")
    while True:
        users_choice = input("Enter: ")
        if users_choice.lower() in ("food", "drinks", "sides", "basket"):
            print(f"You have selected {users_choice.capitalize()}.\n")
            print(f"Loading {users_choice.capitalize()} menu.....\n")
            break
        print("\nInvalid menu option. Please enter valid menu name.")
        print("i.e - Food - Sides - Drinks - Basket - \n")
    return users_choice.lower()


def selected_menu(menu_choice):
    """
    This function takes the input from the user in menu_selection
    and displays the menu the user has selected.
    """
    menu_items = SHEET.worksheet(menu_choice).row_values(1)
    menu_prices = SHEET.worksheet(menu_choice).row_values(2)
    index = 1
    menu_list = []
    print(f"Menu: - {menu_choice.capitalize()} -\n")
    for item, price in zip(menu_items, menu_prices):
        print(f"Item.{index} - {item} : €{price}")
        index += 1
        menu_list.append([index, item, price])
    print(menu_list)
    return menu_list


def menu():
    home_screen()
    menu_choice = menu_selection()
    selected_menu(menu_choice)


menu()
