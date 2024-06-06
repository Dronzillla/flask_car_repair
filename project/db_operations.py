from project import db
from project.models import Customer, Car


# Create new customer
def db_create_customer(first_name: str, last_name: str, email: str, phone: str) -> bool:
    """Tries to create a new customer in database.
    Each customer in database has a unique email address.
    If provided email does not exist in database, customer gets created.
    Otherwise, no new customer is created.

    Args:
        first_name (str): Customer first name
        last_name (str): Customer last name
        email (str): Customer email address
        phone (str): Customer phone number that starts with '+370' and have additional 8 numbers. E.g. +37012345678

    Returns:
        bool: True - Customer with provided email does not exist, False - Customer with provided email exist
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
    customer = Customer.query.filter_by(email=email).one_or_none()
    return customer


# Check if customer with owner_id exists in database
# if db_owner_id_exists(owner_id):
def db_create_car(make: str, model: str, year: int, plate: str, owner_id: int) -> Car:
    # Check if car with provided plate exists
    if db_car_by_plate(plate=plate) is not None:
        return False  # Car with provided plate already exists, so we should not create a new one
    # Create new car
    car = Car(make=make, model=model, year=year, plate=plate, owner_id=owner_id)
    db.session.add(car)
    db.session.commit()
    return car


def db_car_by_plate(plate: str) -> Car:
    car = Car.query.filter_by(plate=plate).one_or_none()
    return car
