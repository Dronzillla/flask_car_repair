from project import app
from flask import render_template, request
from project.models import User
from project.forms import CustomerForm, CarForm
from project.db_operations import db_create_customer, db_create_car, db_read_owner_id


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/profile/<username>")
def display_profile(username):
    user = User.query.filter_by(username=username).one()
    return render_template("profile.html", user=user)


@app.route("/about")
def about():
    return render_template("about.html")


# A route to add new customer
@app.route("/add_customer", methods=["GET", "POST"])
def add_customer():
    # Create a form
    form = CustomerForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Get customer data from the form
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            phone = form.phone.data
            # TODO Try to add new customer. Check if email already exist
            db_create_customer(
                first_name=first_name, last_name=last_name, email=email, phone=phone
            )
        # TODO Write message Customer added successfully.
        return render_template("add_customer.html", form=form)
    # GET request
    return render_template("add_customer.html", form=form)


# A rotue to add new car
@app.route("/add_car", methods=["GET", "POST"])
def add_car():
    # Create a form
    form = CarForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Get car data from the form
            make = form.make.data
            model = form.model.data
            year = form.year.data
            email = form.email.data
            # Get owner id
            owner_id = db_read_owner_id(email=email)
            if owner_id == None:
                # TODO Write message No car owner exists.
                return render_template("add_car.html", form=form)
            # Add car to owner
            db_create_car(make=make, model=model, year=year, owner_id=owner_id)
            # TODO Write message Car added successfully.
            return render_template("add_car.html", form=form)
    # GET request
    return render_template("add_car.html", form=form)
