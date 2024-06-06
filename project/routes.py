from project import app
from flask import render_template, request
from project.forms import CustomerForm, CarForm
from project.db_operations import db_create_customer, db_read_owner_id, db_create_car


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/add_customer", methods=["GET", "POST"])
def add_customer():
    form = CustomerForm()
    if request.method == "POST":
        if form.validate_on_submit():
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
                return render_template(
                    "add_car.html",
                    form=form,
                    message="No can owner exists with provided email exist",
                )
            # Add car to an owner
            db_create_car(make=make, model=model, year=year, owner_id=owner_id)
            # TODO Write message Car added successfully.
            return render_template(
                "add_car.html", form=form, message="Car added successfully"
            )
    # GET request
    return render_template("add_car.html", form=form)
