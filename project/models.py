from project import db


class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    cars = db.relationship("Car", back_populates="owner", cascade="all, delete-orphan")

    def __str__(self):
        return (f"first name: {self.first_name}, last name: {self.last_name})


class Car(db.Model):
    __tablename__ = "car"

    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    plate = db.Column(db.String(80), unique=True, nullable=False)
    owner_id = db.Column(
        db.Integer, db.ForeignKey("customer.id", ondelete="CASCADE"), nullable=False
    )
    owner = db.relationship("Customer", back_populates="cars")

    # Many to Many Car-Service
    car_services = db.relationship("CarServiceAssociation", back_populates="car")

    def __str__(self):
        return f"make: {self.make}, model: {self.model}, year: {self.year}, plate: {self.plate}"


class Service(db.Model):
    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    cost = db.Column(db.Float(), nullable=False)

    # Many to Many Car-Service
    car_services = db.relationship("CarServiceAssociation", back_populates="service")

    def __str__(self):
        return f"name: {self.name}, cost: {self.cost}, description: {self.description}"


# Association Model for Many-to-Many Relationships
class CarServiceAssociation(db.Model):
    __tablename__ = "car_service"

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(
        db.Integer, db.ForeignKey("car.id", ondelete="CASCADE"), nullable=False
    )
    service_id = db.Column(
        db.Integer, db.ForeignKey("service.id", ondelete="CASCADE"), nullable=False
    )
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    car = db.relationship("Car", back_populates="car_services")
    service = db.relationship("Service", back_populates="car_services")


#     __table_args__ = (
#         db.UniqueConstraint(
#             "car_id", "service_id", "date", "time", name="_car_service_date_time_uc"
#         ),
#     )
