from project import app
from flask import render_template, request
from project.forms import CustomerForm, CarForm
from project.db_operations import (
    db_create_customer,
    db_create_car,
    db_find_customer_by_email,
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


# A route to add a new customer
@app.route("/add_customer", methods=["GET", "POST"])
def add_customer():
    form = CustomerForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Get customer data from the form
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            phone = form.phone.data
            # Try to add new customer
            success = db_create_customer(
                first_name=first_name, last_name=last_name, email=email, phone=phone
            )
            if success:
                return render_template(
                    "add_customer.html", message="Registration successfull.", form=form
                )
            else:
                return render_template(
                    "add_customer.html",
                    message="Registration failed. Customer with the following email already exists.",
                    form=form,
                )
    # GET request
    return render_template("add_customer.html", form=form)


# A route to add a new car
@app.route("/add_car", methods=["GET", "POST"])
def add_car():
    form = CarForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Get car data from the form
            make = form.make.data
            model = form.model.data
            year = form.year.data
            email = form.email.data
            plate = form.plate.data
            # Get customer id associated with an email
            customer = db_find_customer_by_email(email=email)
            if customer == None:
                return render_template(
                    "add_car.html",
                    form=form,
                    message="Registration failed. No customer with provided email address exists. ",
                )
            owner_id = customer.id
            # Try to add a new car
            success = db_create_car(
                make=make, model=model, year=year, plate=plate, owner_id=owner_id
            )
            if success:
                return render_template(
                    "add_car.html", message="Registration successfull. ", form=form
                )
            else:
                return render_template(
                    "add_car.html",
                    message="Registration failed. Car with the following plate number already exists. ",
                    form=form,
                )
    # GET request
    return render_template("add_car.html", form=form)
