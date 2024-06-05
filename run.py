from project import app, db
from project.models import User


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

    # CREATE
    # new_user = User(
    #     username="john.doe",
    #     first_name="John",
    #     last_name="Doe",
    #     email="john.doe@example.com",
    # )
    # db.session.add(new_user)
    # db.session.commit()

    # # READ
    # # Read one
    # # read_user = User.query.filter_by(id=1).one()
    # read_user = db.session.get(User, 1)
    # print(read_user)

    # # UPDATE
    # user_obj = db.session.get(User, 1)
    # user_obj.email = "doejohn@example.com"
    # db.session.commit()
    # print(user_obj.email)

    # # DELETE
    # user_obj = db.session.get(User, 1)
    # db.session.delete(user_obj)
    # db.session.commit()
    # print(User.query.all())
