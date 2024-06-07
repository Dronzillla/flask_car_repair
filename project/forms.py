# Classes of forms (code similiar to models.py)
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    IntegerField,
    EmailField,
    DateField,
    TimeField,
    SelectMultipleField,
)
from wtforms.validators import DataRequired, Email, Regexp, NumberRange
from project.db_operations import db_view_service_names


class CustomerForm(FlaskForm):
    first_name = StringField(
        "First Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "First name"},
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired()], render_kw={"placeholder": "Last name"}
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )
    phone = StringField(
        "Phone",
        validators=[
            DataRequired(),
            Regexp(r"^\+370\d{8}$", message="Invalid phone number"),
        ],
        render_kw={"placeholder": "Phone"},
    )
    submit = SubmitField("Submit")


class CarForm(FlaskForm):
    make = StringField(
        "Make", validators=[DataRequired()], render_kw={"placeholder": "Make"}
    )
    model = StringField(
        "Model", validators=[DataRequired()], render_kw={"placeholder": "Model"}
    )
    year = IntegerField(
        "Year",
        validators=[
            DataRequired(),
            NumberRange(min=1900, max=2024, message="Invalid year"),
        ],
        render_kw={"placeholder": "Year"},
    )
    email = EmailField(
        "Owner Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Owner email"},
    )

    plate = StringField(
        "Plate",
        validators=[
            DataRequired(),
            Regexp(
                r"(^[A-Z]{3}\d{3}$)|(^E[A-Z]\d{4}$)", message="Invalid plate number"
            ),
        ],
        render_kw={"placeholder": "Plate"},
    )

    submit = SubmitField("Submit")


class ServiceForm(FlaskForm):
    common_render_kw = {
        "size": 20,
        "style": "width: 200px;",
    }  # Common size and style for all fields

    email = EmailField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={**common_render_kw, "placeholder": "Email"},
    )
    plate = StringField(
        "Plate",
        validators=[
            DataRequired(),
            Regexp(
                r"(^[A-Z]{3}\d{3}$)|(^E[A-Z]\d{4}$)", message="Invalid plate number"
            ),
        ],
        render_kw={**common_render_kw, "placeholder": "Plate"},
    )

    date = DateField(
        "Date",
        validators=[DataRequired()],
        render_kw={**common_render_kw, "placeholder": "Date"},
    )

    time = TimeField(
        "Time",
        validators=[DataRequired()],
        render_kw={**common_render_kw, "placeholder": "Time"},
    )
    services = SelectMultipleField(
        "Services",
        choices=db_view_service_names(),
        validators=[DataRequired()],
        render_kw={**common_render_kw, "placeholder": "Services"},
    )
    submit = SubmitField("Submit")
