from project import db


# Association Table for Many-to-Many Relationship
car_service_association = db.Table(
    "car_service",
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column("car_id", db.Integer, db.ForeignKey("car.id")),
    db.Column("service_id", db.Integer, db.ForeignKey("service.id")),
    db.Column("date", db.Date, nullable=False),
    db.Column("time", db.Time, nullable=False),
)


class Customer(db.Model):
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    cars = db.relationship("Car", back_populates="owner", cascade="all, delete-orphan")

    def __str__(self):
        return f"first name: {self.first_name}, last name: {self.last_name}, email: {self.email}, phone: {self.phone}"


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

    services = db.relationship(
        "Service", secondary=car_service_association, back_populates="cars"
    )

    def __str__(self):
        return f"make: {self.make}, model: {self.model}, year: {self.year}, plate: {self.plate}"


class Service(db.Model):
    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    cost = db.Column(db.Float(), nullable=False)

    cars = db.relationship(
        "Car", secondary=car_service_association, back_populates="services"
    )

    def __str__(self):
        return f"name: {self.name}, cost: {self.cost}, description: {self.description}"
