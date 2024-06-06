# Classes of forms (code similiar to models.py)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, EmailField
from wtforms.validators import DataRequired, Email, Regexp, NumberRange


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
