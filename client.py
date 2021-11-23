import csv
import requests
import json
import random

sess = requests.Session()


def load_menu():
    """ Initially load the menu into the database
    """
    menu = open("Menu.csv")
    var2 = csv.reader(menu)
    list = []
    header = next(menu)
    for row in var2:
        list.append(row)
    menu.close()

    for row in list:
        id = int(row[0])
        half_price = int(row[1])
        full_price = int(row[2])
        data = {"id": id, "half_price": half_price, "full_price": full_price}
        response = sess.post(
            "http://localhost:8000/createMenu", json=data).content
        print(response)


def try_luck(total_amt):
    """Generate a random number between range 1-100.
    Depending on that determine the discount or increase value of the bill.
    """
    random_num = random.randint(1, 100)
    if random_num <= 5:
        dis_percent = -50
    elif random_num > 5 and random_num <= 15:
        dis_percent = -25
    elif random_num > 15 and random_num <= 30:
        dis_percent = -10
    elif random_num > 30 and random_num <= 50:
        dis_percent = 0
    elif random_num > 50:
        dis_percent = 20

    dis_amt = (dis_percent * total_amt) / 100
    if dis_amt == 0:
        print("No change in Price")
    elif dis_amt > 0:
        print("{:<25}{:.2f}".format("Increase in amount:", dis_amt))
    elif dis_amt < 0:
        print("{:<25}{:.2f}".format("Deccrease in amount:", dis_amt))
    """Print pattern"""
    if dis_percent == -50 or dis_percent == -25 or dis_percent == -10:
        print(" ****\t\t ****\n|    |\t\t|    |\n|    |\t\t|    |")
        print("|    |\t\t|    |\n ****\t\t ****\n\t  {}\n      __________")
    elif dis_percent == 0 or dis_percent == 20:
        print(" ****\n*    *\n*    *\n*    *\n ****")

    return dis_amt


def display_menu():
    response = sess.get("http://localhost:8000/readMenu").content
    try:
        dict = json.loads(response)
        print("ID\tHalf\tFull")
        for key, val in dict.items():
            print(key, "\t", val["half_price"], "\t", val["full_price"])
    except:
        print(response)


def add_item_in_menu():
    id = int(input("Enter Item ID: "))
    half_price = int(input("Enter Half Plate Price: "))
    full_price = int(input("Enter Full Plate Price: "))
    data = {"id": id, "half_price": half_price, "full_price": full_price}
    response = sess.post(
        "http://localhost:8000/addMenu", json=data).content
    print(response)


def display_all_transactions():
    response = sess.get("http://localhost:8000/readOrder").content
    dict = json.loads(response)
    print("ID\tHalf_Quan\tFull_Quan")
    for key, val in dict.items():
        print(key, "\t", val["half_quantity"],
              "\t\t", val["full_quantity"])


def signup():
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    data = {"username": username, "password": password}
    response = sess.post(
        "http://localhost:8000/signUp", json=data).content
    print(response)


def login():
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    data = {"username": username, "password": password}
    response = sess.post(
        "http://localhost:8000/login", json=data).content
    print(response)


def logout():
    response = sess.get("http://localhost:8000/logOut").content
    print(response)


def place_order():
    """Takes the order and generates the bill"""
    try:
        n = int(input("Enter how many items do you want to Order?: "))
        for i in range(n):
            id = int(input("Enter Item ID: "))
            plate_type = input("Enter Plate type <half/full>: ")
            quantity = int(input("Enter Quantity: "))
            data = {"id": id, "plate_type": plate_type, "quantity": quantity}
            response = sess.post(
                "http://localhost:8000/addItem", json=data).content

        response3 = sess.get("http://localhost:8000/readOrder").content
        orderDict = json.loads(response3)
        response2 = sess.get("http://localhost:8000/readMenu").content
        MenuDict = json.loads(response2)
        total = 0
        for key, val in orderDict.items():
            amt_half = val["half_quantity"]*MenuDict[key]["half_price"]
            amt_full = val["full_quantity"]*MenuDict[key]["full_price"]
            total = total+amt_half+amt_full

        print("Enter Tip percentage: <0%, 10%, 20%> :", end="\t")
        tip = int(input()[:-1])
        tip_amt = (tip * total) / 100
        total_amt = total + tip_amt
        print("Total Amount:\t", total_amt)

        print("\nEnter number of people to split the Bill :", end="\t")
        people = int(input())
        share = total_amt / people
        print("{}{:.2f}".format("Share of each person: ", share))

        print("\nWant to participate in 'Test your luck' event?", end="")
        cch = input(" <yes/no> :")
        dis_percent = 0
        if cch == "yes":
            dis_percent = try_luck(total_amt)
        orderString = ""
        for key, val in orderDict.items():
            amt_half = val["half_quantity"]*MenuDict[key]["half_price"]
            amt_full = val["full_quantity"]*MenuDict[key]["full_price"]
            if(amt_half != 0):
                orderString = orderString+"Item "+str(
                    key)+" [half] ["+str(val["half_quantity"]) + "] : "+str(
                        amt_half)+"\n"
            if(amt_full != 0):
                orderString = orderString+"Item "+str(
                    key)+" [full] ["+str(val["full_quantity"]) + "] : "+str(
                        amt_full)+"\n"

        print(orderString, "\n")
        print("{:<25}{:.2f}".format("Total:", total))
        print("{:<25}{}%".format("Tip Percentage:", tip))
        print("{:<25}{:.2f}".format("Discount/Increase:", dis_percent))
        final_total = total + dis_percent + tip_amt
        print("{:<25}{:.2f}".format("Final Total:", final_total))
        share = final_total / people
        print("{:<25}{:.2f}".format("Share of each person:", share))
        data = {"total": round(total, 2), "tip": tip, "discount": dis_percent,
                "share": round(share, 2), "amount": round(final_total, 2),
                "items": orderString}
        response4 = sess.post(
            "http://localhost:8000/saveBill", json=data).content
        print(response4)
    except:
        print(response)


def show_bills():
    """Show all the bills of a particular customer"""
    response = sess.get("http://localhost:8000/showAllBill").content
    try:
        users = json.loads(response)
        for key, val in users.items():
            print(key)
        transacID = int(input("Enter what bill to see: "))
        data = {"transactionID": transacID}
        response = sess.get(
            "http://localhost:8000/displayBill", json=data).content
        billDict = json.loads(response)
        print(billDict[str(transacID)]['items'])
        print("Total: ", billDict[str(transacID)]['total'])
        print("Tip Percentage: ", billDict[str(transacID)]['tip'], "%")
        print("Discount: ", billDict[str(transacID)]['discount'])
        print("Final Total: ", billDict[str(transacID)]['amount'])
        print("Share of each person: ", billDict[str(transacID)]['share'])
    except:
        print(response)


load_menu()
while True:
    print("\n---------------------------")
    print("1. Sign Up")
    print("2. Login")
    print("3. Display Menu")
    print("4. Add item to Menu")
    print("5. Place Order")
    print("6. Logout")
    print("7. Show all Bills")
    print("8. Exit")
    print("-----------------------------")

    choice = int(input("Enter choice:"))
    if choice == 1:
        signup()
    if choice == 2:
        login()
    if choice == 3:
        display_menu()
    if choice == 4:
        add_item_in_menu()
    if choice == 5:
        place_order()
    if choice == 6:
        logout()
    if choice == 7:
        show_bills()
    if choice == 8:
        break
