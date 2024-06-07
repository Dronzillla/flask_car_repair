from project import app
from flask import render_template, request
from project.forms import CustomerForm, CarForm, ServiceForm
from project.db_operations import (
    db_create_customer,
    db_create_car,
    db_find_customer_by_email,
    db_find_car_by_plate,
    db_update_car,
    db_update_customer,
    db_view_cars,
    db_view_customers,
    db_view_services,
    db_check_car_ownership,
    db_find_service_by_name,
    db_add_service,
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
                    message="Registration failed. Customer with the following email already exists in database.",
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
                    message="Registration failed. No customer with provided email address exists in database. ",
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
                    message="Registration failed. Car with the following plate number already exists in database. ",
                    form=form,
                )
    # GET request
    return render_template("add_car.html", form=form)


@app.route("/update_customer", methods=["GET", "POST"])
def update_customer():
    form = CustomerForm()
    if request.method == "POST":
        # Get customer data from the form
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        phone = form.phone.data
        # Get customer id associated with an email
        customer = db_find_customer_by_email(email=email)
        # If no customer exist update fails.
        if customer == None:
            return render_template(
                "update_customer.html",
                form=form,
                message="Update failed. No customer with provided email address exists in database. ",
            )
        # If customer with provided email exists. Update information.
        db_update_customer(
            customer=customer,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        return render_template(
            "update_customer.html",
            form=form,
            message="Update successfull. ",
        )
    # GET request
    return render_template("update_customer.html", form=form)


@app.route("/update_car", methods=["GET", "POST"])
def update_car():
    form = CarForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Get car data from the form
            make = form.make.data
            model = form.model.data
            year = form.year.data
            email = form.email.data
            plate = form.plate.data
            # Check for plate number in database
            car = db_find_car_by_plate(plate)
            # If plate number exists update car information and write a message
            if car:
                # Validate customer email
                customer = db_find_customer_by_email(email=email)
                # If customer email is invalid
                if customer == None:
                    return render_template(
                        "update_car.html",
                        form=form,
                        message="Update failed. No customer with provided email address exists in database. ",
                    )
                # If customer email is valid
                owner_id = customer.id
                db_update_car(
                    car=car, make=make, model=model, year=year, owner_id=owner_id
                )
                return render_template(
                    "update_car.html",
                    form=form,
                    message="Update successfull. ",
                )
            # If plate does not exist in database, dont update and write message
            else:
                return render_template(
                    "update_car.html",
                    form=form,
                    message="Update failed. No such car exists in database. ",
                )
    # GET request
    return render_template("update_car.html", form=form)


@app.route("/view_customers")
def view_customers():
    customers = db_view_customers()
    return render_template("view_customers.html", customers=customers)


@app.route("/view_cars")
def view_cars():
    cars = db_view_cars()
    return render_template("view_cars.html", cars=cars)


@app.route("/services", methods=["GET", "POST"])
def services():
    form = ServiceForm()
    all_services = db_view_services()

    if request.method == "POST":
        # Get form data
        email = form.email.data
        plate = form.plate.data
        date = form.date.data
        time = form.time.data
        service_names = form.services.data
        ownership_approved = db_check_car_ownership(email=email, plate=plate)

        # print(type(date))
        # print(type(time))

        if ownership_approved:
            # # Search for a car
            car = db_find_car_by_plate(plate=plate)
            # Make bookings for each service
            for service_name in service_names:
                service = db_find_service_by_name(service_name)
                id = db_add_service(car=car, service=service, date=date, time=time)
            return render_template(
                "services.html",
                services=all_services,
                form=form,
                message="Booking scheduled successfully. ",
            )
        else:
            return render_template(
                "services.html",
                services=all_services,
                form=form,
                message="Booking failed. No car owner with provided car plate number is in the database. ",
            )
    # GET request
    return render_template("services.html", services=all_services, form=form)
