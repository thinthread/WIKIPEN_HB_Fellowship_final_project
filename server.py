from jinja2 import StrictUndefined

# from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, redirect, request, flash,
                  session, jsonify)
from flask_sse import sse

from model import (User, EventLog, StockPen, Image,
                   connect_to_db, db)

# from model import connect_to_db, db

from sqlalchemy import or_

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
# sse = server-sent events.
app.register_blueprint(sse, url_prefix='/stream')


# # Normally, if you use an undefined variable in Jinja2, it fails
# # silently. This is horrible. Fix this so that, instead, it raises an
# # error.
app.jinja_env.undefined = StrictUndefined
app.debug = True
app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # # Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

connect_to_db(app)

    # Use the DebugToolbar
DebugToolbarExtension(app)


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

    if session.get("login"):
        session.pop("login")

    flash("You have been successfully logged out.")

    return redirect("/")


@app.route("/pen_posts")
def pen_posts():
    """Page that shows all posts about pens"""

    # users = User.query.all()
    login = session.get('login')
    return render_template("pen_posts.html", login=login)


@app.route("/create_pen_post_form", methods=["POST"])
def create_pen_post_form():
    """Create new pen post form"""

    # image = request.form.get("image")
    pen_name = request.form.get("pen_name")
    brand_name = request.form.get("brand_name")
    production_start_year = request.form.get("prodection_start_year")
    production_end_year = request.form.get("production_end_year")
    pen_production_version = request.form.get("pen_production_version")
    general_info = request.form.get("general_info")
    pen_type = request.form.get("pen_type")


    login = session.get('login')

    if pen_name:

        _pen = db.session.query(StockPen.pen_title).filter_by(pen_title=pen_name).first()

        if _pen:

            flash("Sorry that specific pen name has already been created. \
                   Please choose another another. Thank you!")

            return redirect("/create_pen_post_form")

        else:

            new_pen_post = StockPen(pen_title=pen_name,
                                    manufacturer=brand_name,
                                    start_year=production_start_year,
                                    end_year=production_end_year,
                                    pen_version=pen_production_version,
                                    general_info=general_info,
                                    pen_category=pen_type)

            db.session.add(new_pen_post)
            db.session.commit()
            flash("You have successfully created a new pen post!")
            return render_template("/pen_posts.html", login=login)

    else:

        return render_template("create_pen_post_form.html", login=login)


@app.route("/show_search_results")
def show_search_results():
    """Search and retrieve data for user to see post"""

    # pen_title = StockPen.query.get(2)

    # return render_template("show_search_results.html", pen_title=pen_title)

    search = request.args.get("brand_name")  # manufacturer

    #pens = StockPen.query.filter_by(manufacturer=search).all()
    pens = StockPen.query.filter(or_(
        StockPen.manufacturer.contains(search),
        StockPen.pen_version.contains(search),
        StockPen.pen_category.contains(search),
        StockPen.pen_title.contains(search))).all()

    return render_template("show_search_results.html", pens=pens)


@app.route("/pens/<int:pen_id>", methods=["GET"])
def pen(pen_id):
    """Render single pen, show detail, hidden option to update pen detail"""

    #print session
    #print session["login"]


    pen = StockPen.query.get(pen_id)

    #login = session.get("login")


    return render_template("pen.html", pen=pen)

@app.route("/update_pen", methods=['POST'])
def update_pen():

        # update_image = request.form.get("image")
    pen_name = request.form.get("pen_name")
    brand_name = request.form.get("brand_name")
    production_start_year = request.form.get("production_start_year")
    production_end_year = request.form.get("production_end_year")
    pen_production_version = request.form.get("pen_production_version")
    general_info = request.form.get("general_info")
    pen_type = request.form.get("pen_type")

    s_pen_id = request.form.get("pen_id")

    pen_to_update = StockPen.query.get(int(s_pen_id))

    if pen_name:

        pen_to_update.pen_title = pen_name
        pen_to_update.manufacturer = brand_name
        pen_to_update.start_year = production_start_year
        pen_to_update.end_year = production_end_year
        pen_to_update.pen_version = pen_production_version
        pen_to_update.pen_category = pen_type
        pen_to_update.general_info = general_info

    db.session.commit()

    sse.publish({"id": s_pen_id, 
        "brand_name": brand_name,
        "start_year": production_start_year,
        "name": pen_name}, type='edit')

    return redirect("/pens/%s" % s_pen_id)


# @app.route("/pen_detail/<int:pen_id>")
# def pen_detail(pen_id):
#     """Show pen detail"""

#     pen = StockPen.query.get(pen_id)

#     return render_template("pen_detail.html", pen=pen)  # pen=pen





    # else:

    #     flash("Hmmm...It seems that the item you are looking for is not part \
    #            of our data-base just yet or is under a different name. \
    #            Please try your search again. Thank you!")

    #     return render_template("pen_posts.html")


# @app.route("/search_retrieve")
# def search_retrieve():
#     """Show search_retrieve screen"""

#     # pen_title = StockPen.query.filter_by(pen_title=).first()

#     # pen_title = StockPen.query.get(2)

#     # return render_template("search_retrieve.html",pen_title=pen_title)




# @app.route("/auto_complete_search.json")     ######### fuzzy search
# def auuto_complete_search_json

######## when doing ajax request pass in paramiters
######## js thing = name

# search = db.session.query(Stockpen).filter_by(StockPen.pen_title.like("%%")).all() % pen_name\
#                         or (Stockpen.manufacturer.like("%%s%")) % brand_name \
#                         # or (Stockpen.start_year.like("%%d%")).all() % production_start_year \
#                         or (Stockpen.pen_version.Like("%%s%")).a() % pen_production_version \
#                         or (Stockpen.general_info.like("%%s%")).all() % general_info \
#                         or (Stockpen.pen_category.like("%%s%")).all() % pen_type \


# @app.route("/update", methods=["POST"])
# def update():
#     """Search and retrieve data base for posts"""

#     return render_template("pen_posts.html")


# @app.route("/delete", methods=["POST"])
# def delete():
#     """Search and retrieve data base for posts"""

#     return render_template("pen_posts.html")





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.run(port=5000, host='0.0.0.0')


