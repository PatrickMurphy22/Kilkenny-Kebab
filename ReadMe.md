# Kilkenny Kebab

## Overview

Welcome to kilkenny Kebab. Kilkenny Kebab is a fictional kebab shop in Kilkenny city.
The idea for this project came from my love of kebabs and my overuse of the JustEat app.

This project was deployed using Heroku and is operated through the Code Institute mock terminal.
My Goal with this project was to keep the ordering process simple and to keep the user in a continuous loop.
The loop is only exited out of when the user completes their order. 
I wanted to keep the process as realistic as possible by adding estimated delivery times and delivery fee's etc.

[Kilkenny Kebab Live Website here](https://kilkennykebab.herokuapp.com/)

# Table of Contents

____

1. [Flow Chart](#flow-chart)
2. [User Experience](#user-experience)
    * [Welcome User & Menu Choice](#welcome-user-&-menu-choice)
    * [Select Items](#select-items)
    * [View Basket](#view-basket)
        * [Add More Items](#add-more-items)
        * [Remove Items](#remove-items)
        * [Checkout](#checkout)
    * [Collection or Delivery](#collection-or-delivery)   
        * [Delivery](#delivery)
        * [Collection](#collection)
3. [Technologies](#technologies)
    * [PYTHON](#python)
    * [JAVASCRIPT](#javascript) 
    * [GOOGLE SHEETS](#google-sheets)  
    * [GOOGLE CLOUD](#google-cloud)
4. [Testing](#testing)

5. [Bugs](#bugs) 
6. [Credits](#credits)
7. [Acknowledgement](#acknowledgement)

---

# Flow Chart



---

# User Experience 

The user experince was at the forefront of my planning and implimentation of my code. 
I executed this by making the ordering process simple and straightforward.

## Welcome User & Menu Choice

The first thing the user see's is a welcoming text and immeditately tells the users to enter the menu name they wish to view.

<!-- PHOTO OF WELCOME SCREEN -->

## Select Items 

After the user selects the menu they want to view, a list of menu items apear to the user. The user is then asked to enter a menu 
item numbers. If the user selects a valid item number they are informed this item in placed into their basket. The user is promted to enter
either the menu name of the menu they wish to order more items for or to view their current basket.

If the users input is invalid they are promted to enter a valid item number

<!-- PHOTO OF SELECT ITEMS -->

## View Basket

If the user selects 'View', their basket is displayed on the terminal with corresponding item numbers.
The user is then given 3 options
    1. Add more items
    2. Remove items
    3. Checkout 

### Add More Items

Its as simple as it sounds. If the user selects 'Add' they are then brought back to the Menu Choice option.

### Remove Items

Again its simple. If the user selects 'Rem' The user is asked to enter the item number of the item they wish to remove from their basket. 
After removing the item The user is shown their new basket and the View Basket step is repeated.

### Checkout 

If the user is happy with their basket and they enter 'Out', they are then taken to the checkout menu.

<!-- PHOTO OF VIEW BASKET ITEMS-->

## Collection Or Delivery

This first step of teh checkout process.

The user is asked wether they wish to collect their food or if they want the food delivered for an additional fee of €3.5.
The user must enter 'C' for collection or 'D' for delivery. 

### Delivery

If the user selects 'D', 2 possible outcomes can occur.

Outcome 1: If the users basket is over the value of €15 the user continues to the next step which involves them entering their EirCode.
           After the user confirms their EirCode they are then given an estimated time based off the time they placed their order.

<!-- PHOTO OF Delivery-->

Outcome 2: If the users basket is under the value of €15 the user is informed that Kilkenny Kebab don't do deliverys for under €15. 
           The user is then asked if they want to order more items to bring their basket value up, if the user enters 'O' They are 
           brought back to Menu Choice. Else if the user enter 'C' they get diverted to  food collection option.

<!-- PHOTO OF invalid basket value-->

### Collection 

If the user selects 'C'. They are informed of the approx time the food will be ready to be collected. 


<!-- PHOTO OF collection-->

---

## Technologies

### Python 

### JavaScript

### Google Sheets

### Google Cloud

--- 
