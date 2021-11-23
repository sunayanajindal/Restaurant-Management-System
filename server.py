from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask import request, session
from flask import Flask
from flask_session import Session

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:sunayana@localhost/menu"
app.config["SECRET_KEY"] = "password"
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.config["SESSION_SQLALCHEMY"] = db
sess = Session(app)
chef = "sunayana"


class Menu(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    half_price = db.Column(db.Integer)
    full_price = db.Column(db.Integer)

    def __init__(self, id, half_price, full_price):
        self.id = id
        self.half_price = half_price
        self.full_price = full_price


class Order(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    half_quantity = db.Column(db.Integer)
    full_quantity = db.Column(db.Integer)

    def __init__(self, id, half_quantity, full_quantity):
        self.id = id
        self.half_quantity = half_quantity
        self.full_quantity = full_quantity


class SignUp(UserMixin, db.Model):
    username = db.Column(db.String(40), primary_key=True)
    password = db.Column(db.String(40))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Bill(UserMixin, db.Model):
    transactionID = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.String(40))
    tip = db.Column(db.String(40))
    discount = db.Column(db.String(40))
    amount = db.Column(db.String(40))
    share = db.Column(db.String(40))
    items = db.Column(db.String(100))

    def __init__(self, total, tip, discount, amount, share, items):
        self.total = total
        self.tip = tip
        self.discount = discount
        self.amount = amount
        self.share = share
        self.items = items


class Transaction(UserMixin, db.Model):
    transactionID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40))

    def __init__(self, transactionID, username):
        self.transactionID = transactionID
        self.username = username


@app.route("/createMenu", methods=["POST"])
def create_Menu():
    data = request.get_json()
    id = data["id"]
    half_price = data["half_price"]
    full_price = data["full_price"]
    resp = Menu.query.filter_by(id=id).first()
    if resp:
        return "id already exists"
    else:
        data = Menu(id, half_price, full_price)
        db.session.add(data)
        db.session.commit()
        return "added successfully"


@app.route("/addMenu", methods=["POST"])
def add_item_Menu():
    if session.get("username") == chef:
        data = request.get_json()
        id = data["id"]
        half_price = data["half_price"]
        full_price = data["full_price"]
        resp = Menu.query.filter_by(id=id).first()
        if resp:
            return "id already exists"
        else:
            data = Menu(id, half_price, full_price)
            db.session.add(data)
            db.session.commit()
            return "added successfully"
    elif session.get("username") is None:
        return "Please login first"
    else:
        return "You are not allowed to add item"


@app.route("/readMenu", methods=["GET"])
def read():
    if session.get("username") is not None:
        data = Menu.query.all()
        resp = {}
        for row in data:
            resp[row.id] = {"half_price": row.half_price, "full_price": row.full_price}
        return resp
    else:
        return "Please Login to read the menu"


@app.route("/addItem", methods=["POST"])
def create_Transaction():
    data = request.get_json()
    if session.get("username") is not None:
        id = data["id"]
        plate_type = data["plate_type"]
        quantity = data["quantity"]
        resp = Order.query.filter_by(id=id).first()
        if resp:
            if plate_type == "half":
                resp.half_quantity = resp.half_quantity + quantity
            elif plate_type == "full":
                resp.full_quantity = resp.full_quantity + quantity
            db.session.commit()
            return "Update Success"
        else:
            if plate_type == "half":
                data = Order(id, quantity, 0)
            else:
                data = Order(id, 0, quantity)
            db.session.add(data)
            db.session.commit()
            return "added successfully"
    else:
        return "Please login to order"


@app.route("/readOrder", methods=["GET"])
def readt():
    data = Order.query.all()
    resp = {}
    for row in data:
        resp[row.id] = {
            "half_quantity": row.half_quantity,
            "full_quantity": row.full_quantity,
        }
    return resp


@app.route("/signUp", methods=["POST"])
def signUp():
    data = request.get_json()
    if session.get("username") is None:
        username = data["username"]
        password = data["password"]
        resp = SignUp.query.filter_by(username=username).first()
        if resp:
            return "Id already exists"
        else:
            data = SignUp(username, password)
            db.session.add(data)
            db.session.commit()
            return "added successfully"
    else:
        return "Please logout and try again"


@app.route("/login", methods=["POST"])
def set_session():
    data = request.get_json()
    usr = data["username"]
    pswd = data["password"]
    if session.get("username") is None:
        resp = SignUp.query.get(usr)
        if resp:
            if pswd == resp.password:
                session["username"] = usr
                return "login successfully"
            else:
                return "login failed--Invalid password"
        else:
            return "Id does not exist. Please Signup"
    else:
        if session.get("username") == usr:
            return "Already logged in"
        else:
            return "Someother user is logged in"


@app.route("/logOut", methods=["GET"])
def logout():
    if session.get("username") is None:
        return "No user is Logged In"
    else:
        session.pop("username", None)
        return "You are logged out"


@app.route("/saveBill", methods=["POST"])
def save_bill():
    data = request.get_json()
    total = data["total"]
    tip = data["tip"]
    discount = data["discount"]
    amount = data["amount"]
    share = data["share"]
    items = data["items"]
    data = Bill(total, tip, discount, amount, share, items)
    db.session.add(data)
    db.session.commit()
    db.session.flush()
    tra_ID = data.transactionID
    usr = session.get("username")
    data = Transaction(tra_ID, usr)
    db.session.add(data)
    db.session.commit()
    db.session.query(Order).delete()
    db.session.commit()
    return "Bill Saved"


@app.route("/showAllBill", methods=["GET"])
def show_bills():
    if session.get("username") is not None:
        data = Transaction.query.filter_by(username=session.get("username"))
        if data is not None:
            resp = {}
            for row in data:
                resp[row.transactionID] = {"username": row.username}
            return resp
        else:
            return "Customer has not placed any order yet"
    else:
        return "Please Login to view"


@app.route("/displayBill", methods=["GET"])
def disp():
    data = request.get_json()
    transactionID = data["transactionID"]
    data = Bill.query.get(transactionID)
    resp = {}
    resp[data.transactionID] = {
        "items": data.items,
        "total": data.total,
        "tip": data.tip,
        "discount": data.discount,
        "amount": data.amount,
        "share": data.share,
    }
    return resp


if __name__ == "__main__":
    app.run(port=8000, debug=True)
