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
    they wish to view.
    """
    print("Menu options: - Food - Sides - Drinks -")
    while True:

        menu_choice = input("Enter: ")

        if menu_choice.lower() in ("food", "drinks", "sides"):

            print(f"You have selected {menu_choice.capitalize()}.\n")
            print(f"Loading {menu_choice.capitalize()} menu.....\n")
            display_selected_menu(menu_choice)
            break

        print("\nInvalid menu option. Please enter valid menu name.")
        print("i.e - Food - Sides - Drinks - \n")


def display_selected_menu(menu_choice):
    """
    This function takes the input from the user in menu_selection
    and displays the menu the user has selected.
    """
    menu_items = SHEET.worksheet(menu_choice).row_values(1)
    menu_prices = SHEET.worksheet(menu_choice).row_values(2)
    index = 0
    menu_list = []

    print(f"---- {menu_choice.capitalize()} ----\n")
    for item, price in zip(menu_items, menu_prices):
        index += 1
        print(f"Item.{index} - {item} : €{price}")
        menu_list.append([index, item, price])
    print("\nEnter the item No. you wish to place into basket.")
    select_menu_items(menu_list)


def select_menu_items(menu_list):
    """
    This function allows the user to select an item
    from the menu_list and update it to the basket worksheet.
    """
    users_basket = SHEET.worksheet("basket")
    user_pick = int(input("Item Number: "))

    for index, item, price in menu_list:
        if user_pick == index:
            users_basket.update_cell(1, 1, item)
            users_basket.update_cell(2, 1, price)
            print(f"You selected Item Number: {index}\n")
            print(f"Adding {item} to basket......")

    order_or_continue()


def view_basket():
    """
    This function lets the user see what items
    are in their basket and the total value
    of the items.
    """
    basket_items = SHEET.worksheet("basket").row_values(1)
    basket_prices = SHEET.worksheet("basket").row_values(2)
    basket_float_price = [float(price) for price in basket_prices]
    total_basket_value = sum(basket_float_price)
    index = 0
    print("\n---- Your Basket ----\n ")
    for item, price in zip(basket_items, basket_float_price):
        index += 1
        print(f"Item.{index} - {item} : €{price}")
    print(f"Total Value: €{total_basket_value}")
    order_or_continue()
    return total_basket_value


def order_or_continue():
    """
    This function asks the user wether they would like
    to add more items to their basket or continue to
    the next step of the proccess.
    """
    print("\nWould you like to order more items?")
    print("Enter Yes to order more or No to view basket.")

    while True:
        yes_no = input("Enter: ")
        if yes_no.lower() == "yes":
            menu_selection()
            break
        if yes_no.lower() == "no":
            break
        print("Thats an invalid input, please enter: Yes or No")
    return False


def collection_or_delivery(total_value):
    """
    This function lets the user select wether they would like
    to collect their order or have the food delivered.
    """
    print("\nDo yo want your order for Collection or Delivery?")
    print("Enter D for delivery or C for collection.")
    print("Delivery cost's €3.5 extra.")
    while True:
        order_method = input("Enter: ")
        if order_method.lower() == "d":
            food_for_delivery(total_value)
            break
        if order_method.lower() == "c":
            print("Thank you for ordering from us.")
            print(f"Your total order cost = {total_value} ")
            print("Your food will be ready for collection at approx.")
            print("Collection Time: ")
            break
        print("Thats an invalid input please enter 'D' or 'C'.")
    return False

def food_for_collection()


def food_for_delivery(total_value):
    """
    This function asks the user for their Eirode twice
    to verify if they entered it correctly, then adds €3.5
    to the total cost of the delivery fee
    and gives estimated time of delivery.
    """
    print("\nYou are nearly there.")
    print("Please enter your Eircode below")

    while True:
        eir_code = input("Eircode: ")
        confirm_eir_code = input("Please confirm Eircode: ")
        if eir_code == confirm_eir_code:
            print("Thank you very much for ordering from us.")
            print(f"Your total order cost = {total_value + 3.5} ")
            print("Your estimated time of delivery will be.")
            print("Delivery Time: ")
            break
        print("Your Eircode's didnt match.")
        print("Please try again..\n")
    return False


def menu():

    home_screen()
    menu_selection()
    total_value = view_basket()
    collection_or_delivery(total_value)


menu()
