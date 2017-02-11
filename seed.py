"""Utility file to seed database"""

from sqlalchemy import func
from model import Users
# from model import EventLog
# from model import StockPens
# from model import VersionPens
# from model import PenTypes
# from model import Images

from model import connect_to_db, db
from server import app
import datetime


def load_users():
    """Load users from u.users into database."""

    # print "Users"

    # # Delete all rows in table, so if we need to run this a second time,
    # # we won't be trying to add duplicate users
    User.query.delete()

    for user in users:
        user = Users(user_id=user_id,
                     first_name=first_name,
                     last_name=last_name,
                     password=password)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_event_log():
    """Load user info from create and edit mode from u.event_log into database."""


    #     db.session.add()
    # db.session.commit()


def load_stock_pens():
    """Load stock pen info from create and edit mode from u.event_log into database"""


    #     db.session.add()
    # db.session.commit()


def version_pens():
    """Version pen stuff here"""
    # """Set value for the next user_id after seeding database"""


    # db.session.execute(query, {'new_id': max_id + 1})
    # db.session.commit()


def pen_types():


def images():


if __name__ == "__main__":
    connect_to_db(app)

    # # In case tables haven't been created, create them
    db.create_all()

    # # Import different types of data
    load_users()
    # load_log_events()
    # load_stock_pens()
    # version()
