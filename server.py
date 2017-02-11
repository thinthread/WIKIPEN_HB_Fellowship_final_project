from jinja2 import StrictUndefined


from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, redirect, request, flash,
                  session, jsonify)

from model import (User, EventLog, StockPen, Image,
                   connect_to_db, db)

from model import connect_to_db, db

app = Flask(__name__)

# # Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# # Normally, if you use an undefined variable in Jinja2, it fails
# # silently. This is horrible. Fix this so that, instead, it raises an
# # error.
app.jinja_env.undefined = StrictUndefined


########################### VIEWS ###############################

@app.route("/")
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/register_form")
def display_register_form():
    """Display register form"""

    return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def register():
    """Register user"""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    if db.session.query(User.user_id_email).filter_by(user_id_email=email).first():
        flash("Sorry the email has already been registered.")
        return redirect("/login_form")

    else:
        new_user = User(first_name=first_name,
                         last_name=last_name,
                         user_id_email=email,
                         password=password)

        db.session.add(new_user)
        db.session.commit()
        flash("You are successfully registered!")
        return render_template("homepage.html")


@app.route("/login_form", methods=["GET"])
def display_login_form():
    """Display lonin form"""

    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def login():
    """Login and display appropriate message"""

    email = request.form.get("email")
    password = request.form.get("password")
    user_info = User.query.filter_by(user_id_email=email).first()

    if user_info:
        # user_id = user_info.user_id_email
        if user_info.password == password:
            flash("Successfully logged in!")
            session["login"] = user_info.user_id_email
            return redirect("/pen_posts")

        else:
            flash("Wrong Password")
            return render_template("login_form.html")
    else:
        flash("User not found!")
        return render_template("login_form.html")


@app.route("/logout", methods=["GET"])
def logout_screen():
    """Display logout from form"""

    return render_template("logout.html")


@app.route("/logout", methods=["POST"])
def logout():
    """Display logout screen"""

    if not session.get("login"):
        session.pop("login")

    flash("You have been successfully logged out.")

    return redirect("/")


@app.route("/pen_posts")
def pen_posts():
    """Page that shows all posts about pens"""

    # users = User.query.all()
    login = session.get('login')
    return render_template("pen_posts.html", login=login)
    # return render_template("create_pen_post_form.html")


@app.route("/create_pen_post_form", methods=["POST"])
def create_pen_post_form():
    """Create new pen post form"""

#     image = request.form.get("image")
#     pen_name = request.form.get("pen_name")
#     brand_name = request.form.get("brand_name")
#     production_start_year = request.form.get("prodection_start_year")
#     production_end_year = request.form.get("production_end_year")
#     pen_prodcution_version = request.form.get("pen_prodcution_version")
#     general_info = request.form.get("general_info")
#     pen_type = request.form.get("pen_type")

#     if db.session.query(StockPen.pen_title).filter_by(pen_title=pen_name).first():
#         flash("Sorry that specific pen name has already been created. \
#                Please choose another another. Thank you!")
#         return redirect("/create_pen_post_form")


#     else:
#         print image


#     #     new_pen_post = StockPen(image=image,
#     #                             pen_name=pen_name,
#     #                             brand_name=brand_name,
#     #                             production_start_year=production_start_year,
#     #                             production_end_year=production_end_year,
#     #                             pen_prodcution_version=pen_prodcution_version,
#     #                             general_info=general_info,
#     #                             pen_type=pen_type)


# # (self.pen_title,
# #  self.manufacturer,
# #  self.start_year,
# #  self.end_year,
# #  self.general_info,
# #  self.pen_category,
# #  self.pen_version)



#         # db.session.add(new_pen_post)
#         # db.session.commit()
#         flash("You have successfully created a new pen post!")
#         return render_template("pen_posts.html")



    return render_template("create_pen_post_form.html")

    # return page back of form
    # can you return form in basic html template?
    # ask how for can be returned







if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')
