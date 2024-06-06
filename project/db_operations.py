from project import db
from project.models import Customer, Car


# Create new customer
def db_create_customer(first_name: str, last_name: str, email: str, phone: str) -> bool:
    """Tries to create a new customer in a database.
    Each customer in database has a unique email address.
    If provided email does not exist in database, customer gets created.
    Otherwise, no new customer is created.

    Args:
        first_name (str): Customer first name
        last_name (str): Customer last name
        email (str): Customer email address
        phone (str): Customer phone number that starts with '+370' and have additional 8 numbers. E.g. +37012345678

    Returns:
        bool: 'True' - Customer with provided email does not exist, 'False' - Customer with provided email exist
    """

    # Check if customer with email provided exists
    if db_find_customer_by_email(email) is not None:
        return False  # Customer already exists, so we should not create a new one
    # Create new customer
    customer = Customer(
        first_name=first_name, last_name=last_name, email=email, phone=phone
    )
    db.session.add(customer)
    db.session.commit()
    return True


# Check if customer with email exists
def db_find_customer_by_email(email: str) -> Customer:
    """Checks for customer in database based on an email address, which is unique.

    Args:
        email (str): Customer email

    Returns:
        Customer: 'Customer' object if customer exists in database, 'None' if customer does not exist in database.
    """
    customer = Customer.query.filter_by(email=email).one_or_none()
    return customer


# Check if customer with owner_id exists in database
def db_create_car(make: str, model: str, year: int, plate: str, owner_id: int) -> Car:
    """Tries to create new car in a database.
    Each car in database has a unique plate number.
    If provided car plate does not exist in database, car gets created.
    Otherwise, no new car is created.

    Args:
        make (str): Car make
        model (str): Car model
        year (int): Car production year
        plate (str): Car plate number. Valid plate number is 3 uppercase letters and 3 numbers or 2 letters starting with E and 4 numbers. E.g. GPI123, EV1563
        owner_id (int): Customer id in database

    Returns:
        Car: 'Car' object if new car is created, 'False' if car plate already exists in database.
    """

    # Check if car with provided plate exists
    if db_find_car_by_plate(plate=plate) is not None:
        return False  # Car with provided plate already exists, so we should not create a new one
    # Create new car
    car = Car(make=make, model=model, year=year, plate=plate, owner_id=owner_id)
    db.session.add(car)
    db.session.commit()
    return car


def db_find_car_by_plate(plate: str) -> Car:
    """Checks for car plate in database based on plate number, which is unique.

    Args:
        plate (str): Car plate number

    Returns:
        Car: 'Car' object if car is found in database, 'None' if car doess not exist in database.
    """
    car = Car.query.filter_by(plate=plate).one_or_none()
    return car


def db_update_car(car: Car, make: str, model: str, year: int, owner_id: int) -> None:
    car.make = make
    car.model = model
    car.year = year
    car.owner_id = owner_id
    db.session.commit()


def db_update_customer(
    customer: Customer, first_name: str, last_name: str, phone: str
) -> None:
    customer.first_name = first_name
    customer.last_name = last_name
    customer.phone = phone
    db.session.commit()
