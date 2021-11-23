# Assignment 3B – Flask and SQLAlchemy

## Signup, Login, Logout
- Every customer will have his/her own account and new customers have the ability to create new ones. 
- These accounts are stored in sign_up database
- Non logged in users can only access signup and login routes

## Display Menu
- The menu is read from a csv file and stored in the menu database.
- Menu is in format ("Item no.", "Half plate price", "Full plate price")
- It is displayed in tab separated format after the user login.

## Adding Items to the Menu
- One static account for chef have been created.
- Only the user who login with the chef's username is allowed to add new items in the menu.

## Input
The user is first prompted to input the number of dishes that he wishes to order
- The user has the input the Item no, plate type and the quantity for each item.
- The input for tip is to be entered along with a percentage sign (%)

## Test your luck event
The user is asked to enter whether he/she wants to participate in the event. The input should be in small case letters as "yes" or "no"
- If "yes", a random number is generated that computes the discount or increase amount on the overall bill
- The pattern is printed only in the case when user inputs "yes"
- If user inputs "no", the discount amount is set to 0.00 and directly the bill is generated.
- The increase amount is a positive value. Hence, no sign is displayed before it.
- The discount amount is displayed with a negative sign.

## Bill
- The total breakdown of the bill (Including the tip) is displayed in the specified format and all the values are rounded upto 2 decimal places.
- The bill details and the transaction ID is saved in the transaction and bill table corresponding to the username.

## View previous bill statements
- The user will be displayed all the past bill record transaction IDs.
- Thw user is asked to select a ID and the bill corresponding to it is displayed.
