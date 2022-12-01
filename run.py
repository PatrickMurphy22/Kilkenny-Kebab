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


def home_screen():
    """
    This function welcomes the user to the home
    screen of Kilkenny Kebab. Then it
    instructes the user on how to progress.
    """
    col = 1
    print("Welcome to Kilkenny Kebab.")
    print("We were voted Ireland's No.1 Kebab shop in 2022. ")
    print("To view our menu's please enter the menu's name below.\n")
    return col


def menu_selection(col):
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
            display_selected_menu(menu_choice, col)
            break

        print("\nInvalid menu option. Please enter valid menu name.")
        print("i.e - Food - Sides - Drinks - \n")
    return False


def display_selected_menu(menu_choice, col):
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
    add_items_to_basket(menu_list, col)


def add_items_to_basket(menu_list, col):
    """
    This function allows the user to select an item
    from the menu_list and update it to the basket worksheet.
    """
    users_basket = SHEET.worksheet("basket")
    user_pick = int(input("Item Number: "))

    for index, item, price in menu_list:
        if user_pick == index:
            row = 1
            users_basket.update_cell(row, col, item)
            row += 1
            users_basket.update_cell(row, col, price)
            print(f"You selected Item Number: {index}\n")
            print(f"Adding {item} to basket......")
            col += 1
    view_basket(col, users_basket)


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
    print("\n---- Your Basket ----\n ")
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
    basket()
    print(f"Total Value: €{calculate_total_basket_value()}")
    alter_basket(col, users_basket)


def alter_basket(col, users_basket):
    """
    This function lets the user remove items
    from their basket and asks the user if they
    would like to add more items.
    """

    print("\nWould you like to make any changes to your basket??\n")
    print("Enter Add to add more items, or Rem to remove items.")
    print("If neither please Enter Out to continue to checkout.\n")

    while True:
        users_choice = input("Enter: ")
        if users_choice.lower() == "add":
            print("")
            menu_selection(col)
            break
        if users_choice.lower() == "rem":
            remove_basket_items(col, users_basket)
            break
        if users_choice.lower() == "out":
            break
    return False


def remove_basket_items(col, users_basket):
    """
    This function lets the user select what item they
    would like to remove from their basket.
    """
    print("\nPlease enter the item num you want to remove.")
    basket()
    remove_item = int(input("\nRemove Item Number: "))
    for num in range(col):
        if remove_item == num:
            users_basket.update_cell(1, num, "")
            users_basket.update_cell(2, num, "")
            
    print(f"\nitem Number {remove_item} has been removed from your basket.")


def collection_or_delivery(total_value, current_time):
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
            food_for_delivery(total_value, current_time)
            break
        if order_method.lower() == "c":
            food_for_collection(total_value, current_time)
            break
        print("Thats an invalid input please enter 'D' or 'C'.")

    return False


def food_for_collection(total_value, current_time):
    """
    Tells user when food will be ready for collection
    and gives total basket value.
    """
    collection_time = current_time + timedelta(minutes=20)

    print("Thank you for ordering from us.")
    print(f"Total price: {total_value} ")
    print("Your food will be ready for collection at approx.")
    print(f"Estimated Collection Time: {collection_time} ")


def food_for_delivery(total_value, current_time):
    """
    This function asks the user for their Eirode twice
    to verify if they entered it correctly, then adds €3.5
    to the total cost of the delivery fee
    and gives estimated time of delivery.
    """
    delivery_time = current_time + timedelta(minutes=40)
    delivery_fee = total_value + 3.50

    print("\nYou are nearly there.")
    print("Please enter your Eircode below")

    while True:
        eir_code = input("Eircode: ")
        confirm_eir_code = input("Confirm Eircode: ")
        if eir_code == confirm_eir_code:
            print(f"\nYour food will be delivered to Eircode: {eir_code}")
            print(f"Total price: €{delivery_fee}\n")
            print(f"Esitmated Delivery Time: {delivery_time}")
            break
        print("Eircode's didnt match.")
        print("Please try again..\n")
    return False


def menu():

    current_time = time()
    col = home_screen()
    menu_selection(col)
    total_value = calculate_total_basket_value()
    collection_or_delivery(total_value, current_time)


menu()
