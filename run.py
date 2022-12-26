from datetime import datetime, timedelta
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


def time():

    now = datetime.now()
    current_time = now - timedelta(microseconds=now.microsecond)
    return current_time


def column_value():
    col = 1
    return col


def home_screen():
    """
    This function welcomes the user to the home
    screen of Kilkenny Kebab. Then it
    instructes the user on how to progress.
    """
    SHEET.worksheet("basket").clear()
    print("Welcome to Kilkenny Kebab.")
    print("We were voted Ireland's No.1 Kebab shop in 2022.")
    print("To view our menu's please enter the menu's name below.\n")


def menu_selection(col):
    """
    This function will allow users to select either the menu
    they wish to view.
    """
    print("      Menu Options")
    options = "- Food - Sides - Drinks -"
    print(options)

    while True:
        menu_choice = input("Enter: \n")
        selected_menu = menu_choice.lower()

        if selected_menu in ("food", "drinks", "sides"):
            print(f"You have selected {selected_menu.capitalize()}.\n")
            display_selected_menu(selected_menu, col)
            break

        print(f"\n{selected_menu} is not an option.")
        print(f"Please select from {options}")

    return False


def display_selected_menu(selected_menu, col):
    """
    This function takes the input from the user in menu_selection
    and displays the menu the user has selected.
    """
    print(f"Loading {selected_menu.capitalize()} menu.....\n")

    menu_items = SHEET.worksheet(selected_menu).row_values(1)
    menu_prices = SHEET.worksheet(selected_menu).row_values(2)
    index = 0
    menu_list = []
    print(f"---- {selected_menu.capitalize()} Menu ----\n")

    for item, price in zip(menu_items, menu_prices):
        index += 1
        print(f"Item.{index} - {item} : €{price}")
        menu_list.append([index, item, price])

    print("\nEnter the item No. you wish to place into basket.")
    add_items_to_basket(menu_list, col)


def add_items_to_basket(menu_list, col):
    """
    This function allows the user to select an item
    from the menu_list and update it to the basket worksheet.
    """
    users_basket = SHEET.worksheet("basket")
    while True:
        try:
            user_pick = int(input("item number: \n"))
            if user_pick <= 7 and user_pick >= 1:
                break
            print("Invalid item number.")
        except ValueError:
            print("That is not a number. Please try again")

    for index, item, price in menu_list:

        if user_pick == index:
            row = 1
            users_basket.update_cell(row, col, item)
            row += 1
            users_basket.update_cell(row, col, price)
            print(f"You selected Item {index} : {item} €{price}")
            print("Adding to basket......\n")
            col += 1
            view_basket_or_order_more(col, users_basket)
            break


def view_basket_or_order_more(col, users_basket):
    opt_1 = "To order more items, enter the menu's name."
    opt_2 = "To view your basket and continue enter 'View'."
    print(opt_1)
    print(opt_2)

    while True:

        choice = input("Enter: \n")
        selected_menu = choice.lower()

        if selected_menu in ("food", "sides", "drinks"):
            display_selected_menu(selected_menu, col)
            break
        if selected_menu == "view":
            view_basket(col, users_basket)
            break

        print("\nInvalid input")
    return False


def calculate_total_basket_value():
    """
    This function calculates the total value of the users basket.
    """
    basket_prices = SHEET.worksheet("basket").row_values(2)
    basket_float_price = [float(price) for price in basket_prices]
    total_basket_value = sum(basket_float_price)
    return total_basket_value


def basket():
    """
    This function holds the contents of the users basket.
    """
    basket_items = SHEET.worksheet("basket").row_values(1)
    basket_prices = SHEET.worksheet("basket").row_values(2)
    index = 0
    for item, price in zip(basket_items, basket_prices):
        index += 1
        print(f"Item.{index} - {item} : €{price}")


def view_basket(col, users_basket):
    """
    This function lets the user see what items
    are in their basket and the total value
    of the items.
    """
    calculate_total_basket_value()
    print("\n---- Your Basket ---- ")
    basket()
    print(f"\nTotal Value: €{calculate_total_basket_value()}")
    alter_basket(col, users_basket)


def alter_basket(col, users_basket):
    """
    This function lets the user remove items
    from their basket and asks the user if they
    would like to add more items.
    """
    print("\nWould you like to make any changes to your basket??\n")
    print("Enter 'Add' to add more items, or 'Rem' to remove items.")
    print("If neither please Enter 'Out' to continue to checkout.\n")

    while True:
        users_choice = input("Enter: \n")
        if users_choice.lower() == "add":
            print("")
            menu_selection(col)
            break
        if users_choice.lower() == "rem":
            remove_basket_items(col, users_basket)
            break
        if users_choice.lower() == "out":
            collection_or_delivery(col)
            break
        print("Invalid input, please enter 'add', 'rem', or 'out'.")
    return False


def remove_basket_items(col, users_basket):
    """
    This function lets the user select what item they
    would like to remove from their basket.
    """
    print("\nPlease enter the item num you want to remove.")
    while True:
        try:
            remove_item = int(input("Remove item number: \n"))
            if remove_item < col and remove_item >= 1:
                break
            print("That is not a number. Please try again")
        except ValueError:
            print("invalid")
    for num in range(col):
        if remove_item == num:
            users_basket.delete_columns(num)
            print(f"\nRemoving Item No. {remove_item}.")
            print(f"Item Number: {remove_item} has been removed...")
            col -= 1
            users_basket.add_cols(1)
            view_basket(col, users_basket)
            break


def collection_or_delivery(col):
    """
    This function lets the user select wether they would like
    to collect their order or have the food delivered.
    """
    total_value = calculate_total_basket_value()
    basket_value_0(col, total_value)
    print("\nDo yo want your order for Collection or Delivery?")
    print("Enter D for delivery or C for collection.")
    print("Delivery cost's €3.5 extra.")
    print(total_value)
    while True:
        order_method = input("Enter: ")
        order_method_lower = order_method.lower()
        if order_method_lower == "d":
            basket_value_under_15(total_value, col)
            useless_programer(order_method_lower)
            food_for_delivery(total_value)
            break
        if order_method_lower == "c":
            useless_programer(order_method_lower)
            food_for_collection(total_value)
            break
        print("Thats an invalid input please enter 'D' or 'C'.")

    return False


def food_for_collection(total_value):
    """
    Tells user when food will be ready for collection
    and gives total basket value.
    """
    current_time = time()
    collection_time = current_time + timedelta(minutes=20)

    print("Thank you for ordering from us.")
    print(f"Total price: €{total_value} ")
    print("Your food will be ready for collection at approx.")
    print(f"Estimated Collection Time: {collection_time} \n")
    print("Please click on 'Run Program' to order again..")
    SHEET.worksheet("basket").clear()
    exit()


def food_for_delivery(total_value):
    """
    This function asks the user for their Eirode twice
    to verify if they entered it correctly, then adds €3.5
    to the total cost of the delivery fee
    and gives estimated time of delivery.
    """
    current_time = time()
    delivery_time = current_time + timedelta(minutes=40)
    delivery_fee = total_value + 3.50

    print("\nYou are nearly there.")
    print("Please enter your Eircode below")
    print("PS. Eircodes are Case sensitive")

    while True:

        eir_code = input("Eircode: \n")
        confirm_eir_code = input("Confirm Eircode: \n")

        if eir_code == confirm_eir_code:
            print(f"\nYour food will be delivered to Eircode: {eir_code}")
            print(f"Total price: €{delivery_fee}\n")
            print(f"Esitmated Delivery Time: {delivery_time}\n")
            print("Please click on 'Run Program' to order again..")
            SHEET.worksheet("basket").clear()
            exit()

        print("Eircode's didnt match.")
        print("Please try again..\n")
    return False


def useless_programer(order_method_lower):
    print("\nUnfortunately our Web developer is only a rookie, and")
    print("he doesn't know how to implement an online payement system 'yet'.")
    if order_method_lower == "d":
        print("So we only accept cash payment for delivery's.")
    elif order_method_lower == "c":
        print("So you will have to make the payment in store.")
    print("Sorry for the inconvenience.")


def basket_value_under_15(total_value, col):
    """
    This function compares the users basket to the value 15.
    If basket is over 15 user may proceed to checkout for delivery.
    IF basket under 15 user told to order more to increase basket
    value or told to go to collection.
    """
    while True:
        if total_value > 15:
            print(total_value)
            break
        if total_value < 15:
            print(total_value)
            print("As a result of the extortionate price of fuel.")
            print("We only deliver orders over €15.")
            print("if you want to collect your food instead, enter 'c', ")
            print("Else enter 'o' to order more food.\n")
            while True:
                user_choice = input("Enter: \n")
                user_choice_lower = user_choice.lower()
                if user_choice_lower == "c":
                    food_for_collection(total_value)
                    break
                if user_choice_lower == "o":
                    print(col)
                    menu_selection(col)
                    break
    return False


def basket_value_0(col, total_value):
    """
    This function checks if the users basket is 0
    If the basket is 0 it redirects user to order food.
    """
    if total_value == 0:
        print("\nSorry it seems like your basket is empty")
        print("We are redirecting you to our menu's\n")
        menu_selection(col)


def menu():
    """
    This function initiates the program to start and finish.
    """
    col = column_value()
    home_screen()
    menu_selection(col)


menu()
