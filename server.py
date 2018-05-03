from jinja2 import StrictUndefined

# import os
from flask import Flask, request, redirect  # ,url_for
# from werkzeug.utils import secure_filename
# from werkzeug import SharedDataMiddleware
# from werkzeug import secure_filename

from flask import send_from_directory
from flask_sse import sse #flask server sent events powered by redis
from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
# from flask import Flask, Request

from model import (User, StockPen, Image, EventLog, connect_to_db, db)

# import uuid   # for random file name uploads
# import json
# from model import connect_to_db, db
from sqlalchemy import or_
from sqlalchemy import func
from sqlalchemy import distinct

# import gcs_client
# from google.cloud import storage
# storage_client = storage.Client.from_service_account_json('wikipen-86a6bc3c96db.json')

#########from selenium import webdriver

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

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
# DebugToolbarExtension(app)

########################### VIEWS ###############################

# browser = webdriver.Firefox()
# driver = webdriver.Chrome(executable_path=r"C:\Chrome\chromedriver.exe")

# browser.get('http://localhost:5000')
# assert browser.title == 'UberCalc'

# x = browser.find_element_by_id('x-field')
# x.send_keys("3")
# y = browser.find_element_by_id('y-field')
# y.send_keys("4")

# btn = browser.find_element_by_id('calc-button')
# btn.click()

# result = browser.find_element_by_id('result')
# assert result.text == "7"


# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    """Homepage."""

    if index:
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
    """Display login form"""

    return render_template("login_form.html")


@app.route("/login", methods=["POST"])
def login():
    """Login and display appropriate message"""

    email = request.form.get("email")
    password = request.form.get("password")
    print('\n\n\n email: ', email)
    print('\n\n\n password: ', password)
    user_info = User.query.filter_by(user_id_email=email).first()
    print('\n\n\n\n\n', user_info, '\n\n\n\n\n\n')
    if user_info:
        # user_id = user_info.user_id_email
        if user_info.password == password:
            flash("Successfully logged in!")
            session["login"] = user_info.user_id_email
            return redirect("/")

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

# UPLOAD_FOLDER = '/path/to/the/uploads'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# #######   disallow .php files if the server executes them, but who has PHP installed on their server


@app.route("/create_pen_post_form", methods=["POST", "GET"])
def create_pen_post_form():
    """Create new pen post form"""

    login = session.get('login')

    pen_name = request.form.get("pen_name")

    if pen_name:

        pen = db.session.query(StockPen.pen_title).filter_by(pen_title=pen_name).first()

        if pen:
                flash("Sorry that specific pen name has already been created. Please choose another another. Thank you!")

                return redirect("/create_pen_post_form")

        elif pen_name is None:

            flash("Sorry , you must fill out a pen name on this form. Thank you!")
            return redirect("/create_pen_post_form")

        else:

            form_images = request.form.getlist("images")

            brand_name = request.form.get("brand_name")
            production_start_year = request.form.get("production_start_year")
            production_end_year = request.form.get("production_end_year")
            pen_production_version = request.form.get("pen_production_version")
            general_info = request.form.get("general_info")
            pen_type = request.form.get("pen_type")

            new_pen_post = StockPen(pen_title=pen_name,
                                    manufacturer=brand_name,
                                    start_year=production_start_year,
                                    end_year=production_end_year,
                                    pen_version=pen_production_version,
                                    general_info=general_info,
                                    pen_category=pen_type)

            db.session.add(new_pen_post)

            for new_img in form_images:
                new_image = Image(image_url=new_img, pen=new_pen_post)
                db.session.add(new_image)

            db.session.flush()

            new_user = login

            new_event = EventLog(user_id_email=new_user, s_pen_id=new_pen_post.s_pen_id)

            db.session.add(new_event)
            db.session.commit()

            sse.publish({"image_url": new_pen_post.images[0].image_url,
                         "id": new_pen_post.s_pen_id,
                         "brand_name": brand_name,
                         "start_year": production_start_year,
                         "name": pen_name}, type='edit')

            flash("You have successfully created a new pen post!")
            return redirect("/pens/%s" % new_pen_post.s_pen_id)

    else:

        return render_template("create_pen_post_form.html", login=login)

    # import pdb
    # pdb.set_trace()

    # if pen_name:

    #     if img_to_add:   # item in db


        # if request.method == 'POST':
        #     file = request.files['file']
        #     extension = secure_filename(file.filename).rsplit('.', 1)[1]
        #     options = {}
        #     options['retry_params'] = gcs.RetryParams(backoff_factor=1.1)
        #     options['content_type'] = 'image/' + extension
        #     bucket_name = "gcs-tester-app"
        #     path = '/' + bucket_name + '/' + str(secure_filename(file.filename))

        # if file and allowed_file(file.filename):
        #     try:
        #         with gcs.open(path, 'w', **options) as f:
        #             f.write(file.stream.read())  # instead of f.write(str(file))
        #             print jsonify({"success": True})
        #         return jsonify({"success": True})
        #     except Exception as e:
        #         logging.exception(e)
        #         return jsonify({"success": False})


            # if _pen:
            #     if request.method == 'POST':
            #     # check if the post request has the file part
            #         if 'file' not in request.files:
            #             flash('No file part')
            #             return redirect(request.url)
            #         file = request.files['file']
            #         # if user does not select file, browser also
            #         # submit a empty part without filename
            #         if file.filename == '':
            #             flash('No selected file')
            #             return redirect(request.url)
            #         if file and allowed_file(file.filename):
            #             filename = secure_filename(file.filename)
            #             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #             return redirect(url_for('uploaded_file',
            #                                     filename=filename))

            #      # check on LargeGAinary

            #     return '''
            #     <!doctype html>
            #     <title>Upload new File</title>
            #     <h1>Upload new File</h1>
            #     <form method=post enctype=multipart/form-data>
            #       <p><input type=file name=file>
            #          <input type=submit value=Upload>
            #     </form>
            #     '''
        #     # todo dont try to upload a file if it wasnt specified.
        #     file = request.files['image']
        #     if file:
        #         #extension = secure_filename(file.filename).rsplit(".", 1)[1]
        #         # todo randomly choose a name.
        #         path = str(uuid.uuid4())
        #         #path = secure_filename(file.filename)
        #         bucket = storage_client.get_bucket('wikipen')
        #         # blobstore.create_upload_url()

        #         # todo it might not be image/jpeg type
        #         blob.upload_from_string(file.stream.read(), file.content_type)
        #         blob.reload()
        #         url = blob.public_url
        #         print "Image uploaded to: "
        #         print url

@app.route("/update_pen", methods=['POST'])
def update_pen():

    form_images = request.form.getlist("images")

    pen_name = request.form.get("pen_name")
    brand_name = request.form.get("brand_name")
    production_start_year = request.form.get("production_start_year")
    production_end_year = request.form.get("production_end_year")
    pen_production_version = request.form.get("pen_production_version")
    general_info = request.form.get("general_info")
    pen_type = request.form.get("pen_type")

    s_pen_id = int(request.form.get("pen_id"))

    pen_to_update = StockPen.query.get(s_pen_id)

    for img_update in map(None, pen_to_update.images, form_images):
        if img_update[0] is None:
            new_image = Image(image_url=img_update[1], pen=pen_to_update)
            db.session.add(new_image)
        elif img_update[0].image_url != img_update[1]:
            img_update[0].image_url = img_update[1]

    pen_to_update.pen_title = pen_name
    pen_to_update.manufacturer = brand_name
    pen_to_update.pen_version = pen_production_version
    pen_to_update.pen_category = pen_type
    pen_to_update.general_info = general_info

    if production_start_year and production_start_year != "None":
        pen_to_update.start_year = int(production_start_year)
    else:
        pen_to_update.start_year = None

    if production_end_year and production_end_year != "None":
        pen_to_update.end_year = int(production_end_year)
    else:
        pen_to_update.end_year = None

    db.session.flush()

    login = session.get('login')

    new_user = login

    new_event = EventLog(user_id_email=new_user, s_pen_id=pen_to_update.s_pen_id)

    db.session.add(new_event)

    db.session.commit()

    sse.publish({"image_url": pen_to_update.images[0].image_url,
                 "id": s_pen_id,
                 "brand_name": brand_name,
                 "start_year": production_start_year,
                 "name": pen_name}, type='edit')

    return redirect("/pens/%s" % s_pen_id)


@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

        #### register uploaded_file as build_only rule
        #### wsgi- Web Server Gateway Interface - is an interfacebetween a web server & Python web frameworks/applications
        #### The Web Server Gateway Interface (WSGI) is a simple calling convention for web servers to forward requests to 
        #### web applications or frameworks written in the Python programming language. The current version of WSGI, 
        #### version 1.0.1, is specified in Python Enhancement Proposal (PEP) 3333.
        #### Pep, Pep 333 or Pep 3333 is Python's Web Server Gateway Interface
    app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                         build_only=True)
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/uploads':  app.config['UPLOAD_FOLDER']})

@app.route("/pens/<int:pen_id>", methods=["GET"])
def pen(pen_id):
    """Render single pen, show detail, hidden option to update pen detail"""

    pen = StockPen.query.get(pen_id)

    emails = [x.user_id_email for x in pen.events]

    return render_template("pen.html", pen=pen, contributors=set(emails))


@app.route("/last_modified", methods=["GET"])
def last_modified():

    # events = db.session.query(
    #     EventLog.query.distinct(EventLog.s_pen_id).order_by(EventLog.s_pen_id,EventLog.last_time).subquery()
    #     ).order_by(EventLog.last_time.desc()).limit(5)
    # events = db.session.query(EventLog.s_pen_id,
    #     func.max(EventLog.last_time),
    #     func.max(Image.image_url)).join(Image.s_pen_id).group_by(EventLog.s_pen_id).order_by(func.max(EventLog.last_time.desc()))

    pens = StockPen.query.order_by(StockPen.last_time.desc()).limit(5)

    nameurl = []
    for pen in pens:
        nameurl.append({"name": pen.pen_title,
                        "id": pen.s_pen_id,
                        "image_url": pen.images[0].image_url})
    return jsonify(nameurl)


@app.route("/show_search_results", methods=["GET"])
def show_search_results():
    """Search and retrieve data for user to see post"""

    search = request.args.get("brand_name").lower()  # manufacturer
    session["search"] = search

    pens = StockPen.query.filter(or_(
        func.lower(StockPen.manufacturer).contains(search),
        func.lower(StockPen.pen_version).contains(search),
        func.lower(StockPen.pen_category).contains(search),
        func.lower(StockPen.pen_title).contains(search))).all()

    return render_template("show_search_results.html", pens=pens)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension

    # app.run(port=5000, host='0.0.0.0', debug=True)
    app.run(port=5000, host='0.0.0.0')

# to run gunicorn server
# gunicorn server:app --worker-class gevent --bind 0.0.0.0:5000 --reload --graceful-timeout 3
# WSGI web server gateway interface
# default: Fixed port collision for 5000 => 5000. Now on port 2200.
# ==> default: Fixed port collision for 22 => 2222. Now on port 2201.
# ==> default: Forwarding ports...
#     default: 5000 (guest) => 2200 (host) (adapter 1)
