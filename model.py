from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
# from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """User info."""

    __tablename__ = "users"

    user_id_email = db.Column(db.String(20), primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<User user_id_email=%s first_name=%s last_name=%s >" % \
                                                (self.user_id_email,
                                                 self.first_name,
                                                 self.last_name)


class StockPen(db.Model):
    """Details of stock_pens and thier info."""

    __tablename__ = "pens"

    s_pen_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    pen_title = db.Column(db.String(30))
    manufacturer = db.Column(db.String(20))
    start_year = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    general_info = db.Column(db.String(2000))
    pen_category = db.Column(db.String(20))
    pen_version = db.Column(db.String(20))
    last_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    def get_url(self):
        return "/pens/%s" % self.s_pen_id

    def __repr__(self):
        return "<StockPen pen_title=%s manufacturer=%s start_year=%s end_year=%s \
                 general_info=%s pen_category=%s pen_version=%s>" % (self.pen_title,
                                                                     self.manufacturer,
                                                                     self.start_year,
                                                                     self.end_year,
                                                                     self.general_info,
                                                                     self.pen_category,
                                                                     self.pen_version)


class EventLog(db.Model):
    """Track user input events per create or update of a post."""

    __tablename__ = "event"

    event_log_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    last_time = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    user_id_email = db.Column(db.String(20), db.ForeignKey("users.user_id_email"))
    s_pen_id = db.Column(db.Integer, db.ForeignKey("pens.s_pen_id"), index=True)

    user = db.relationship("User", backref=db.backref("events"))

    pen = db.relationship("StockPen", backref=db.backref("events"))

    def __repr__(self):
        return "<EventLog last_time=%s user_id_email=%s s_pen_id=%s>" % (self.last_time,
                                                                         self.user_id_email,
                                                                         self.s_pen_id)


class Image(db.Model):
    """Collect images and tie them back to either Stock_pens or Version_pens."""

    __tablename__ = "images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    image_url = db.Column(db. String(300))
    s_pen_id = db.Column(db.Integer, db.ForeignKey("pens.s_pen_id"))

    pen = db.relationship("StockPen", backref=db.backref("images"), order_by=image_id)

    def __repr__(self):
        return"<Images image_url=%s s_pen_id=%s>" % (self.image_url,
                                                     self.s_pen_id)


# HELPING functions to connect to db and connect flask app to the db.
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///pens'
    ## app.config['SQLALCHEMY_ECHO'] = False
    ## app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)

    db.create_all()

    print "Connected to DB."
